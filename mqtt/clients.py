import paho.mqtt.client as mqtt
import paho.mqtt.publish as pub
import connect
import get
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
        SQL = "SELECT garage_type,garage_num FROM garage_info_table WHERE pub_code='%s'"%topic
        data = connect.sql_not_roll(SQL)
        all_exist_car = ""  #所有车位是否存在车的状态组成的字符串
        if len(data) == 1:
            if data[0][0] == 0:     #升降横移车库
                for i in range(0,len(message)):
                    if i >= 1 and i <= 13:
                        if message[i] == 'n':
                            all_exist_car += '0'
                        elif message[i] == 'y':
                            all_exist_car += '1'
                all_door_state = str(message[14]) + str(message[15]) + str(message[16])#三个门状态组成的字符串,为毛不切片
                """
                不是本来就是字符串的吗，为何str()
                字典也是只需要生成一个的，最终才是组装字典发送到Django,无需写两次的，
                还有替换算法的实现完全有re模块可以承担，两堆字典+两堆算法堆得慌
                算法需要整改
                """
                dict1 = {
                  'garage': data[0][1],
                  'garage_type' : 0,
                  'running_state' : message[0],
                  'exist_car' : all_exist_car,
                  'door_state' : all_door_state,
                  'side_control' : message[17],
                }
                get.send_to_django(dict1)
            elif data[0][0] == 1:   #垂直循环车库
                for i in range(0,len(message)):
                    if i >= 1 and i <= 8:#总共有16个车位，预留了多个位置，暂时只取到8个
                        if message[i] == 'n':
                            all_exist_car += '0'
                        elif message[i] == 'y':
                            all_exist_car += '1'
                dict2 = {
                    'garage': data[0][1],
                    'garage_type' : 1,
                    'running_state' : message[0],
                    'exist_car' : all_exist_car,
                    'door_state' : "1",
                    'side_control' : message[17],
                }
                get.send_to_django(dict2)
        else:
            print("warning:数据重叠错误！")


client = mqtt.Client()
client.username_pw_set("olswxmqtt","olswxappmqtt32219")
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST,1883,60)
#应该去数据库查出所有主题
client.subscribe("C/gds100001/P",2)
'''

client.subscribe([
    ("C/gds100001/P",2),
    ("C/gds100002/P",2)
])

'''#订阅多车库主题的方法

client.loop_forever()



