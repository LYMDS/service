import paho.mqtt.publish as pub

HOST="120.77.156.184"
U_P={"username":"olswxmqtt",
      "password":"olswxappmqtt32219"}

def send(topic,context):
    pub.single(topic,context,
               hostname="localhost",
               qos=2,
               retain=False,
               port=1883,
               auth=U_P)

send("C/gds100001/P","i am your father")
