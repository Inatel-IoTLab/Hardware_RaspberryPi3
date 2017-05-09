import paho.mqtt.client as paho
from time import gmtime, strftime

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
        
        topic="icc_nmc"
        qos = 1
        
        print("Subscribing to the topic %s with QoS %d" %(topic,qos))
        client.subscribe(topic, qos)


def OnDisconnecthandler(client, userdata, rc): 
#       called when the client disconnects from the broker.
#       The rc parameter indicates the disconnection state. If MQTT_ERR_SUCCESS
#       (0), the callback was called in response to a disconnect() call. If any
#       other value the disconnection was unexpected, such as might be caused by
#       a network error.
    print("Disconnection returned" + str(rc))

def OnMessageHandler(client, userdata, message): 
#     called when a message has been received on a
#     topic that the client subscribes to. The message variable is a
#     MQTTMessage that describes all of the message parameters.
    print("###################################")
    print("New message received:")
    print("Topic: " + str(message.topic))
    print("QoS: " + str(message.qos))
    print("Payload: " + str(message.payload))
    print("###################################")

def OnPublishHandler(client, userdata, mid): 
#       called when a message that was to be sent using the
#       publish() call has completed transmission to the broker. For messages
#       with QoS levels 1 and 2, this means that the appropriate handshakes have
#       completed. For QoS 0, this simply means that the message has left the
#       client. The mid variable matches the mid variable returned from the
#       corresponding publish() call, to allow outgoing messages to be tracked.
#       This callback is important because even if the publish() call returns
#       success, it does not always mean that the message has been sent.
    print("Publish approved!")

def OnSubscribeHandler(client, userdata, mid, granted_qos): 
#       called when the broker responds to a
#       subscribe request. The mid variable matches the mid variable returned
#       from the corresponding subscribe() call. The granted_qos variable is a
#       list of integers that give the QoS level the broker has granted for each
#       of the different subscription requests.
    print("Subscribe successful with QoS: " + str(granted_qos))

def OnUnsubscribeHandler(client, userdata, mid): 
#     called when the broker responds to an unsubscribe
#       request. The mid variable matches the mid variable returned from the
#       corresponding unsubscribe() call.
    print("Unsubscription returned ")

def OnLogHandler(client, userdata, level, buf): 
#     called when the client has log information. Define
#       to allow debugging. The level variable gives the severity of the message
#       and will be one of MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING,
#       MQTT_LOG_ERR, and MQTT_LOG_DEBUG. The message itself is in buf.
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
    payload_str = "teste"
    qos = 1
    retain = False
    publish_delay = 15
     
    run = True
    while run:
        client.loop()
        
        if(publish_delay < 1):
            print("Publishing new data on %s" %topic)
            payload = strftime("%a, %d %b %Y %H:%M:%S +0000, ", gmtime()) + payload_str
            client.publish(topic, payload, qos, retain)
            publish_delay=10
        else:    
            publish_delay=publish_delay-1
        print("Remaining time for new publishing: %d" %(publish_delay))
