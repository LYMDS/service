import paho.mqtt.client as mqtt
import paho.mqtt.publish as pub
import connect
from get import send_to_django
HOST = "localhost"

Host = "120.77.156.184"
U_P = {"username": "olswxmqtt",
       "password": "olswxappmqtt32219"}

def send(topic,context):
    pub.single(topic,context,
               hostname=HOST,
               qos=2,
               retain=False,
               port=1883,
               auth=U_P)

def on_connect(client,userdata,flags,rc):
    print("connect succes")
def on_message(client,userdata,msg):
    topic = msg.topic
    message = msg.payload.decode()
    if message[0] == 'S' and message[-1] == 'T':
        message = message.strip('ST')
        topic = topic.rstrip("P") + "S"
        SQL = "SELECT garage_type FROM garage_info_table WHERE pub_code='%s'"%topic
        data = connect.sql_not_roll(SQL)
        if len(data) == 1:
            if data[0][0] == 0:     #升降横移车库
                send_to_django()
            elif data[0][0] == 1:   #垂直循环车库
                send_to_django()
        else:
            print("warning:数据重叠错误！")
    #取数据库的车库类型匹对


client = mqtt.Client()
client.username_pw_set("olswxmqtt","olswxappmqtt32219")
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST,1883,60)
client.subscribe("C/gds100001/P",2)
client.loop_forever()



