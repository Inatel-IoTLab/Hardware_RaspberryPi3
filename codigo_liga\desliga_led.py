import paho.mqtt.client as paho
import RPi.GPIO as GPIO
import time
from time import gmtime, strftime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
LedState = False
aux = False

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
        
        topic="raspberryPi"
        qos = 1
        
        print("Subscribing to the topic %s with QoS %d" %(topic,qos))
        client.subscribe(topic, qos)


def OnDisconnecthandler(client, userdata, rc): 
    print("Disconnection returned" + str(rc))

def OnMessageHandler(client, userdata, message): 

    MensagemRecebida = str(message.payload)
    if MensagemRecebida == "on":
        print "LED on"
        GPIO.output(18,GPIO.HIGH)
        global LedState
        LedState = True

    if MensagemRecebida == "off":
        print "LED off"
        GPIO.output(18,GPIO.LOW)
        global LedState
        LedState = False

    if MensagemRecebida == "state":
        global aux
        aux = True

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
    
    topic = "raspberryPi"
    payload_str = "teste"
    qos = 1
    retain = False
    publish_delay = 15
     
    run = True
    while run:
        client.loop()
        
        if(publish_delay < 1):

            client.on_connect = OnConnectHandler
            client.on_message = OnMessageHandler
            client.connect(host, port, keepalive)

            if aux == True:
                payload = LedState
                client.publish(topic, payload, qos, retain)
                aux = False
            publish_delay=10

            
            
        else:    
            publish_delay=publish_delay-1
      
