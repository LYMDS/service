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

#send("C/gds100001/P","i am your father")
'''---------------------------------------------
import connect
topic = "C/gds100001/P"
topic = topic.rstrip("P")+"S"
SQL = "SELECT garage_type,garage_num FROM garage_info_table WHERE pub_code='%s'"%topic
data = connect.sql_not_roll(SQL)
print(data[0][1])
print(type(data))
print(len(data))
'''
import get
url = "http://120.77.156.184/mqtt_receive"
data = {
    'garage': 1,
    'garage_type' : 0,
    'running_state' : 's',
    'exist_car' : "010100101111",
    'door_state' : "010",
    'side_control' : "f",
}
response = requests.get(url,headers=headers,params=data)
json = response.json()


