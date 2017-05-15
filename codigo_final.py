import paho.mqtt.client as paho
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from time import gmtime, strftime

sensor = Adafruit_DHT.DHT11
GPIO.setmode(GPIO.BOARD)
pino_sensor = 25

def rc_answers_to_strings(argument):
    switcher = {
        0: "Connection successful",
        1: "Connection refused - incorrect protocol version",
        2: "Connection refused - invalid client identifier",
        3: "Connection refused - server unavailable",
        4: "Connection refused - bad username or password",
        5: "Connection refused - not authorised",
        6-255: "Currently unused",
    }
    return switcher.get(argument, "nothing")

def OnConnectHandler(client, userdata, flags, rc):
        print(rc_answers_to_strings(rc))
        
        topic="lab_iot"
        qos = 1
        
        print("Subscribing to the topic %s with QoS %d" %(topic,qos))
        client.subscribe(topic, qos)


def OnDisconnecthandler(client, userdata, rc): 
    print("Disconnection returned" + str(rc))

def OnMessageHandler(client, userdata, message): 
    print("###################################")
    print("New message received:")
    print("Topic: " + str(message.topic))
    print("QoS: " + str(message.qos))
    print("Payload: " + str(message.payload))
    print("###################################")

def OnPublishHandler(client, userdata, mid): 
    print("Publish approved!")

def OnSubscribeHandler(client, userdata, mid, granted_qos): 
    print("Subscribe successful with QoS: " + str(granted_qos))

def OnUnsubscribeHandler(client, userdata, mid): 
    print("Unsubscription returned ")

def OnLogHandler(client, userdata, level, buf): 
    print("Log: " + str(buf))


if __name__ == '__main__':
    
    client = paho.Client()
    
    client.on_connect = OnConnectHandler
    client.on_disconnect = OnDisconnecthandler
    client.on_message = OnMessageHandler
    client.on_subscribe = OnSubscribeHandler
    client.on_publish = OnPublishHandler
    
    host="iot.eclipse.org"
    port = 1883
    keepalive=60
    bind_address=""
    
    print("Trying to connect to %s" %host)
    
    client.connect(host, port, keepalive, bind_address)
    
    topic = "raspberry"
    qos = 1
    retain = False
    publish_delay = 5
    
    run = True
    while run:
       client.loop()
       umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor);                              # Efetua a leitura do sensor
       if umid is not None and temp is not None:
            valores = ("Temperatura = {0:0.1f}  Umidade = {1:0.1f}\n").format(temp, umid);
       if(publish_delay < 1):
            print("Publishing new data on %s" %topic)
            client.publish(topic, valores, qos, retain)
            publish_delay=10
       else:    
            publish_delay=publish_delay-1
       print("Remaining time for new publishing: %d" %(publish_delay))
