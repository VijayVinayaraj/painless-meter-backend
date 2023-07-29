import paho.mqtt.client as mqtt
import json
import psycopg2
import datetime
from fastapi import FastAPI
from uvicorn import run
import multiprocessing
from fastapi.middleware.cors import CORSMiddleware
DATABASE_URL = "postgres://{user}:{password}@{hosturl}:{port}".format(
    user="postgres", password="password", hosturl="192.168.224.229", port=5432
)

app=FastAPI()

consumer1 = "painlessMesh/from/3821661665"
consumer2 ="painlessMesh/from/1375526329"
consumer3 = "painlessMesh/from/1375462669"
consumer4 =""

consumer1pub ="painlessMesh/to/3821661665"
consumer2pub ="painlessMesh/to/1375526329"
consumer3pub ="painlessMesh/to/1375462669"
consumer4pub ="painlessMesh/to/3821661665"



origins = ["*"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def databaseInit():
    querycreateConsumer1 = """CREATE TABLE IF NOT EXISTS consumer1(
                                        time TIMESTAMPTZ NOT NULL,
                                        watthour DOUBLE PRECISION
                                    );
                                    """
    querycreateConsumer2 = """CREATE TABLE IF NOT EXISTS consumer2(
                                        time TIMESTAMPTZ NOT NULL,
                                        watthour DOUBLE PRECISION
                                    );
                                    """
    querycreateConsumer3 = """CREATE TABLE IF NOT EXISTS consumer3(
                                        time TIMESTAMPTZ NOT NULL,
                                        watthour DOUBLE PRECISION
                                    );
                                    """
    querycreateConsumer4 = """CREATE TABLE IF NOT EXISTS consumer4(
                                        time TIMESTAMPTZ NOT NULL,
                                        watthour DOUBLE PRECISION
                                    );
                                    """

    
    databaseInsert(querycreateConsumer1)
    databaseInsert(querycreateConsumer2)
    databaseInsert(querycreateConsumer3)
    databaseInsert(querycreateConsumer4)
    databaseInsert("SELECT create_hypertable('consumer1', 'time');")
    databaseInsert("SELECT create_hypertable('consumer2', 'time');")
    databaseInsert("SELECT create_hypertable('consumer3', 'time');")
    databaseInsert("SELECT create_hypertable('consumer4', 'time');")



def on_connect(mqttc, obj, flags, rc):
    subscribeToALL(mqttc)
    print("rc: "+str(rc))
def on_message(mqttc, obj, msg):
    getDatafrombroker(msg)
    # print(msg.payload)
    # returnDataFromMqttBroker(msg.payload)
def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
def on_disconnect(mqttc,obj,rc):
    print("discoonected reconnecting")
    mqttc.connect('localhost', 1883, 6)


mqttc = mqtt.Client("database")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

# mqttc.connect('mosquitto-docker', 9001, 60)
mqttc.connect('192.168.224.229', 1883, 60)
print(f'trying to connect.....')



def databaseInsert(query):
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        try:
            conn.commit()
        except:
            print("eroor in query")

def insertDataToDB(data,consumerNo):
    values = []
    for value in data.values():
        values.append(value)
    valuesStr = f"'{values[0]}',{values[1]}"
    insert_query = f"INSERT INTO {consumerNo} ({','.join(data.keys())}) VALUES ({valuesStr}) "
    databaseInsert(insert_query)
    print(insert_query)


def returnDataFromMqttBroker(data,consumerNo):
    # print(f"{data} ::: {consumerNo}")
    insertDataToDB(data,consumerNo)



def subscribeToALL(mqtt):
    mqtt.subscribe(consumer1)
    mqtt.subscribe(consumer2)
    mqtt.subscribe(consumer3)
    # mqtt.subscribe(consumer4)

def getDatafrombroker(msg):
    topic = msg.topic
    timestamp = datetime.datetime.now()
    time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    if topic == consumer1:
        data ={"time":str(time),"watthour":msg.payload.decode("utf-8")}
        returnDataFromMqttBroker(data,"consumer1")
    elif topic == consumer2:
        data ={"time":str(time),"watthour":msg.payload.decode("utf-8")}
        returnDataFromMqttBroker(data,"consumer2")
    elif topic == consumer3:
        data ={"time":str(time),"watthour":msg.payload.decode("utf-8")}
        returnDataFromMqttBroker(data,"consumer3")
    elif topic == consumer4:
        data ={"time":str(time),"watthour":msg.payload.decode("utf-8")}
        returnDataFromMqttBroker(data,"consumer4")
    else:
        data=msg.payload.decode("utf-8")
        print(f"data from {type(msg.topic)}  ::{data}")







@app.post("/send/{consumerid}/{state}")
async def send_message(consumerid:int,state:int):
    # Publish the message to the specified topic
    # mqttc.publish(topic, message)
    print(type(consumerid), consumerid , type(state))
    if consumerid == 1 :
        mqttc.publish(consumer1pub,state)
    elif consumerid == 2 :
        mqttc.publish(consumer2pub,state)
    elif consumerid ==3 :
        mqttc.publish(consumer3pub,state)
    elif consumerid == 4:
        mqttc.publish(consumer4pub,state)
    return {"message": "Message sent successfully!"}




def runUvicorn():
    run(app,host="0.0.0.0",port=8080)
def runMqttClient():
    mqttc.loop_forever()
if __name__ == "__main__":
    multiprocessing.Process(target=runUvicorn).start()
    multiprocessing.Process(target=runMqttClient).start()