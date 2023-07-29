import paho.mqtt.client as mqtt
import random
import time
import asyncio


def on_connect(mqttc, obj, flags, rc):
    mqttc.subscribe('painlessMesh/to/broadcast')
    print("rc: "+str(rc))
def on_message(mqttc, obj, msg):
    print(msg.topic)
    # returnDataFromMqttBroker(msg.payload)
def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
def on_log(mqttc, obj, level, string):
    print(string)
def on_disconnect(mqttc,obj,rc):
    print("discoonected reconnecting")
    print(obj)
    print(rc)
    mqttc.connect('localhost', 1883, 6)


mqttc = mqtt.Client("dd")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect
mqttc.on_log = on_log
# mqttc.connect('mosquitto-docker', 9001, 60)
mqttc.connect('192.168.224.229', 1883, 60)
print(f'trying to connect.....')






def senddatatobroker(topic):
    mqttc.publish(topic,str(random.randint(1, 100)))






async def my_function():
    senddatatobroker("painlessMesh/from/3821661665")
    senddatatobroker("painlessMesh/from/1375526329")
    senddatatobroker("painlessMesh/from/1375462669")
    await asyncio.sleep(1)

# Define an asynchronous function to call the main function repeatedly
async def call_function_repeatedly():
    while True:
        await my_function()


if __name__ == "__main__":
    #  databaseInit()
     asyncio.run(call_function_repeatedly())
     mqttc.loop_forever()