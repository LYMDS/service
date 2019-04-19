import paho.mqtt.client as mqtt
import paho.mqtt.publish as pub
HOST = "127.0.0.1"

Host = "120.77.156.184"
U_P = {"username": "olswxmqtt",
       "password": "olswxappmqtt32219"}

def send(topic,context):
    pub.single(topic,context,
               hostname="localhost",
               qos=2,
               retain=False,
               port=1883,
               auth=U_P)

def on_connect(client,userdata,flags,rc):
    print("connect succes")
def on_message(client,userdata,msg):
	print("-------------------------------------------------")
	topic = msg.topic   
	mess = msg.payload.decode()
	print(topic)
	print(mess)
	print("-------------------------------------------------")


client = mqtt.Client()
client.username_pw_set("olswxmqtt","olswxappmqtt32219")
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST,1883,60)
client.subscribe("C/gds100001/P",2)
client.loop_forever()



