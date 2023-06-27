import sys
from Adafruit_IO import MQTTClient
import random as r
import time
import aitest
import requests

AIO_USERNAME = "nttuananh2004"
EQUATION_API = "https://io.adafruit.com/api/v2/nttuananh2004/feeds/equation"
temp = open("key")
AIO_KEY = temp.read()
temp.close()
global_equation = ""

def connected(client):
    print("Successfully connected")
    client.subscribe("button1")
    client.subscribe("button2")
    client.subscribe("equation")

def subscribe(client , userdata , mid , granted_qos):
    print("Successfully subscribed")

def disconnected(client):
    print("Disconecting...")
    sys.exit (1)

def message(client , feed_id , payload):
    global global_equation
    print(f"Received payload from \"{feed_id}\": {payload}")
    if (feed_id == "equation"):
        global_equation = payload

def init_global_equation():
    global global_equation
    headers = {}
    temp = requests.get(url = EQUATION_API, headers = headers, verify = False)
    temp = temp.json()
    global_equation = temp["last_value"]
    print(f"Latest equation value: {global_equation}")

def evaluate(sensor1, sensor2, sensor3):
    result = eval(global_equation)
    print(f"Evaluation result of {global_equation}: {result}")
    return result

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

init_global_equation()
client.connect()
client.loop_background()

while True:
    sensorOneValue = r.randint(0, 80)
    sensorTwoValue = r.randint(0, 100)
    sensorThreeValue = r.randint(0, 10)
    client.publish("sensor1", sensorOneValue)
    time.sleep(4)
    client.publish("sensor2", sensorTwoValue)
    time.sleep(4)
    client.publish("sensor3", sensorThreeValue)
    time.sleep(4)
    client.publish("ai", aitest.imageDetector()) #Homework: Output AI data to Adafruit
    time.sleep(4)
    client.publish("testfeed", evaluate(sensorOneValue, sensorTwoValue, sensorThreeValue))
    time.sleep(10)