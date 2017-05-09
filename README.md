# Hardware_RaspberryPi3
## Conectando Raspberry Pi 3 ao MQTTLens
### Caracteristicas do Raspberry
- Raspberry Pi 3 Model B
- Processador Broadcom BCM2837 64bit ARMv8 Cortex-A53 Quad-Core
- Clock 1.2 GHz
- Memória RAM: 1GB
- Adaptador Wifi 802.11n integrado
- Bluetooth 4.1 BLE integrado
- Conector de vídeo HDMI
- 4 portas USB 2.0
- Conector Ethernet
- Interface para câmera (CSI)
- Interface para display (DSI)
- Slot para cartão microSD
- Conector de áudio e vídeo
- GPIO de 40 pinos
- Dimensões: 85 x 56 x 17mm

![image](https://cloud.githubusercontent.com/assets/26795001/25636568/2b5887d4-2f58-11e7-90ac-651d2f7d2814.png)
![image](https://cloud.githubusercontent.com/assets/26795001/25636940/6d4f5162-2f59-11e7-916c-526d29b72cf5.png)

* [1º Passo: Instalar o Raspbian no Raspberry pi 3:](#passo1)
* [2º Passo: Configurar o Raspberry pi 3 a uma rede:](#passo2)
* [3º Passo: Testando sensor de temperatura e umidade no Raspberry pi 3:](#passo3)
* [4º Passo: Enviando dados do Raspberry pi 3 para o MQTTLens:](#passo4)
* [5º Passo: Mesclando os dois programas](#passo5)

<a name="passo1"></a>
## 1º Passo: Instalar o Raspbian no Raspberry pi 3:
O slot para cartão micro SD é uma parte importante do Raspberry, pois é através de um cartão como esse que iremos instalar o Raspbian, um sistema operacional baseado em Linux e otimizado para uso com o Raspberry. Para instalar o Raspbian no cartão SD ele deve estar vazio.
Vá até a seção de downloads do site oficial do Raspberry Pi Foundation (www.raspberrypi.org) e procure pelo download Raspbian – Raspbian Jessie With Pixel, clique em Download ZIP para baixar o arquivo. Após baixar o arquivo extraia a imagem do Raspbian em uma pasta no computador.

![image](https://cloud.githubusercontent.com/assets/26795001/25637387/2fd73384-2f5b-11e7-96c1-c4a469a5136f.png)

Baixe e instale o utilitário gravador de cartão SD Etcher disponível no link https://etcher.io/ . Execute o Etcher, selecione a imagem do Raspbian extraída, selecione a unidade de cartão micro SD (Talvez o Etcher já tenha selecionado a unidade correta) e logo após clique em flash para instalar o Raspbian no cartão SD. Quando concluído remova o cartão micro SD do computador (é seguro remover o cartão micro SD diretamente porque o Etcher ejeta ou desmonta automaticamente o cartão após a conclusão) e insira o cartão SD no seu Raspberry pi.

![image](https://cloud.githubusercontent.com/assets/26795001/25637476/868213ca-2f5b-11e7-83ee-7ae7129bc5e4.png)

Ligue o Raspberry utilizando uma fonte de alimentação e um cabo micro USB (Observação: É importante usar uma fonte de alimentação do kit que tenha pelo menos 2A para confirmar que o Raspberry será alimentado com capacidade suficiente para funcionar corretamente.).

<a name="passo2"></a>
## 2º Passo: Configurar o Raspberry pi 3 a uma rede:
Em primeiro lugar, deve-se instalar alguns periféricos para facilitar a configuração da placa, tais como: 
•	Teclado USB.
•	Mouse USB.
•	Fonte de alimentação de 5v / 2A com conexão micro USB (Lembre-se que a USB do computador suporta no máximo 500 mA, portanto não ligue o Raspberry diretamente nessa porta).
•	Um monitor de vídeo com entrada HDMI ou DVI.

![image](https://cloud.githubusercontent.com/assets/26795001/25637741/740b5b9c-2f5c-11e7-8a8c-6730c70f87d3.png)

Da versão de novembro de 2016 em diante, o Raspbian tem o servidor SSH desabilitado por padrão. Você precisa habilitá-lo manualmente. Você pode conectar um monitor e ir para Preferências-> Configuração do Raspberry Pi para habilitar o SSH.
Pode-se conectar a Raspberry pi 3 a uma rede com fio ou sem fio. Para conecta-lo a uma rede com fio basta apenas conectar o cabo Ethernet no seu conector, os dois LED’s do pi serão acesos quando a conexão for estabelecida. Para conecta-lo a uma rede sem fio utilizaremos a própria interfase do Raspberry, na área de trabalho do Raspbian, clique no símbolo do Wifi no canto superior direito e conecte-se na rede desejada.

![image](https://cloud.githubusercontent.com/assets/26795001/25637809/a8a7db5a-2f5c-11e7-81b3-596a078e677c.png)

<a name="passo3"></a>
## 3º Passo: Testando sensor de temperatura e umidade no Raspberry pi 3:

Nesse passo vamos monitorar a temperatura e a umidade do sensor DHT 11. Este sensor funciona nas seguintes características:
•	Alimentação: 3 a 5,5 V
•	Faixa de leitura – Umidade: 20 a 80%
•	Precisão umidade: 5%
•	Faixa de leitura – Temperatura: 0 – 50 ºC
•	Precisão temperatura: +/- 2 ºC
O sensor envia os dados para o microcontrolador utilizando apenas um pino, os outros dois são Vcc e GND, sendo que o terceiro pino não é utilizado. Segue a pinagem abaixo:

![image](https://cloud.githubusercontent.com/assets/26795001/25638271/3a08ba64-2f5e-11e7-9531-f705bcc98d45.png)

Vamos enviar os dados do sensor para o Raspberry Pi em intervalos de 20 segundos. Como alimentação, vamos utilizar os 3.3V da placa, e como pino de entrada no Raspberry o pino 22 (GPIO 25).
Não se esqueça que os pinos do Raspberry utilizam nível de tensão de 3.3V, portanto se você for alimentar o DHT11 com uma fonte externa (maior do que 3.3V), por exemplo, é necessário um divisor de tensão para não danificar a GPIO do Raspberry. Utilize um resistor de 4,7 K como pull-up para o pino de dados do sensor.

![image](https://cloud.githubusercontent.com/assets/26795001/25638300/4f4ca6c4-2f5e-11e7-964d-cccce0e6d647.png)

Depois de feita a montagem do DHT11 conectado ao Raspberry realizaremos alguns passos para funcionar	:

•	Passo 1: abrir o LX terminal (prompt de comando) do Raspberry e digitar os seguintes comandos para a instalação da biblioteca do sensor:
```js	
  git clone https://github.com/adafruit/Adafruit_Python_DHT.git
  cd Adafruit_Python_DHT
```

•	Passo 2: antes de terminar a instalação digite os seguintes comandos para atualizar o Raspberry:
```js	
 sudo apt-get update
 sudo apt-get install build-essential python-dev
```

•	Passo 3: para concluir a instalação digite o seguinte comando:
```js
sudo python setup.py install
```
•	Passo 4: abra o python do raspberry (IDL), abra uma nova janela (New Window), digite o seguinte código, salve e pressione F5 para rodar o programa.

```js
# Programa : Sensor de temperatura DHT11 com Raspberry Pi B+
# Autor : FILIPEFLOP
 
# Carrega as bibliotecas
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
 
# Define o tipo de sensor
sensor = Adafruit_DHT.DHT11
#sensor = Adafruit_DHT.DHT22
 
GPIO.setmode(GPIO.BOARD)
 
# Define a GPIO conectada ao pino de dados do sensor
pino_sensor = 25
 
# Informacoes iniciais
print ("*** Lendo os valores de temperatura e umidade");
 
while(1):
   # Efetua a leitura do sensor
   umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor);
   # Caso leitura esteja ok, mostra os valores na tela
   if umid is not None and temp is not None:
     print ("Temperatura = {0:0.1f}  Umidade = {1:0.1f}\n").format(temp, umid);
     print ("Aguarda 20 segundos para efetuar nova leitura...\n");
     time.sleep(20)
   else:
     # Mensagem de erro de comunicacao com o sensor
     print("Falha ao ler dados do DHT11 !!!")
     
```     
*No início do código são carregadas as bibliotecas Adafruit_DHT, para leitura do sensor de temperatura, e também as bibliotecas GPIO e timer.

<a name="passo4"></a>
## 4º Passo: Enviando dados do Raspberry pi 3 para o MQTTLens:

Esse passo será dividido em 3 partes de como instalar e configurar a extensão do google MQTTLens, como baixar o Paho-MQTT (cliente MQTT oficial) no Raspberry e como rodar o programa no python.
### 1ª Parte: pesquisar MQTTLens, baixar e configurar

![image](https://cloud.githubusercontent.com/assets/26795001/25639000/aee57adc-2f60-11e7-80f8-7909663bde23.png)

Depois de baixado e instalado, abra o programa, clique no símbolo “+” no canto superior esquerdo e faça as seguintes configurações: 

![image](https://cloud.githubusercontent.com/assets/26795001/25639033/cc6f852a-2f60-11e7-8a2b-53c1224edbb5.png)

O broker utilizado no exemplo foi o iot.eclipse.org mas pode ser outro do interesse da pessoa. Para criar agora basta clicar em “Create Connection” e abrira a seguinte interface:

![image](https://cloud.githubusercontent.com/assets/26795001/25639055/e63684ae-2f60-11e7-84e9-d3fa5a6ebbc8.png)

Agora em subscribe de um nome para o tópico e clique em “Subscribe”. Lembrando que esse será o nome que irá no código do programa e que poderá ser acessado no mundo todo. Segue o exemplo:

![image](https://cloud.githubusercontent.com/assets/26795001/25639086/fda7cc9c-2f60-11e7-86b9-5f5921c32eb7.png)

A parte do MQTTLens já está pronta agora vamos a 2ª parte.

### 2ª Parte: instalando Paho-MQTT
	
Abra o LX terminal (prompt de comando) do Raspberry e digite os seguintes comandos para clonar o repositório do Paho-MQTT para python.

```js
	git clone https://github.com/eclipse/paho.mqtt.python
	cd paho.mqtt.python
	python setup.py install 
```

Depois desses comandos a instalação do Paho-MQTT está feita e pronta para serem desenvolvidos projetos em python que utilizem o protocolo MQTT.

### 3ª Parte: criando o código

Nessa parte já vamos usar um código pronto, apenas abra o python no Raspberry, crie uma nova janela e digite o seguinte código:

```js
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
        
        topic="IoTLab"
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

```

Depois de digitado pressione F5 e rode o programa. Lembrando que o Raspberry possui duas versões do Python e o programa só vai funcionar o que foi instalado o Paho-MQTT. Na tela do MQTTLens deverá aparecer “testing connection ok” no tópico Raspberry criado.

<a name="passo5"></a>
## 5º Passo: Mesclando os dois programas

Esse é o último passo para o Raspberry Pi 3 conseguir enviar as informações de temperatura e umidade para a extensão MQTTLens, o que vamos fazer agora é apenas juntar os dois programas.
Usando o programa do último passo iremos incluir algumas coisas tais como biblioteca do sensor, qual pino está sendo usado e fazer ler a temperatura e umidade para mandar ao MQTTLens. Depois de feito tudo isso o código ficara assim:

```js
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
        
        topic="IoTLab"
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
    payload_str = "28"
    qos = 1
    retain = False
    publish_delay = 10
    
     
    run = True
    while run:
       client.loop()
       # Efetua a leitura do sensor
       umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor);
       # Caso leitura esteja ok, mostra os valores na tela
       if umid is not None and temp is not None:
                #  time.sleep(20)
         payload_str = ("Temperatura = {0:0.1f}  Umidade = {1:0.1f}\n").format(temp, umid);
         payload = strftime("%a, %d %b %Y %H:%M:%S +0000, ", gmtime()) + payload_str   
       if(publish_delay < 1):
            print("Publishing new data on %s" %topic)
            #payload = strftime("%a, %d %b %Y %H:%M:%S +0000, ", gmtime()) + payload_str
            client.publish(topic, payload_str, qos, retain)
            publish_delay=5
       else:    
            publish_delay=publish_delay-1
       print("Remaining time for new publishing: %d" %(publish_delay))
```

Depois de digitado, salve e pressione F5 para rodar o programa. A cada 5 segundos esse código mandara as informações para o MQTTLens e você vai poder visualizar de qualquer lugar.



