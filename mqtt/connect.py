import pymysql
import paho.mqtt.publish as pub

HOST="localhost"
message_topic="C/gds100002/P"
message_payload="SqbbbbbbbbbbbbbbbbbT"

def send(topic,context): # MQTT的连接函数
    U_P = {'username': "olswxmqtt",
           'password': "olswxappmqtt32219"}
    pub.single(topic,context,
             hostname=HOST,
             port=1883,
             qos=2,
             auth=U_P,
             retain=False,
            keepalive=30)

# 数据库连接函数
def sql_need_roll(sql):
    db = pymysql.connect(HOST,
                          "root",
                          "609586869",
                          "olsdatabase")
    cursor = db.cursor()
    try:
        cursor.execute(sql)# 执行sql语句
        db.commit()# 提交到数据库执行
    except:
        print("sadfsaf")
        db.rollback()# 如果发生错误则回滚
        cursor.close()
        db.close()

def sql_not_roll(sql):
    db = pymysql.connect(HOST,
                         "root",
                         "609586869",
                         "olsdatabase")
    cursor = db.cursor()
    cursor.close()
    db.close()
    return results


def insert_data(message_topic,message_payload):
    sql = """
    INSERT INTO test_log(topic,payload,status) VALUES(%s,%s,%s)
    """%(message_topic,message_payload,"MQTT代码服务器已收到")
    sql_need_roll(sql)

insert_data(message_topic,message_payload)
