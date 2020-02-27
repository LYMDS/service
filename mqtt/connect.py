import pymysql
import paho.mqtt.publish as pub

HOST="localhost"
#HOST="120.77.156.184"
#由于测试方便，可选HOST
U_P = {'username': "olswxmqtt",
           'password': "olswxappmqtt32219"}

def send(topic,context): # MQTT的连接函数
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
        print("SQL语句出错，自动回滚")
        db.rollback()# 如果发生错误则回滚
        cursor.close()
        print("回滚完毕")
        db.close()

def sql_not_roll(sql):
    db = pymysql.connect(HOST,
                         "root",
                         "609586869",
                         "olsdatabase")
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results


'''
def insert_data(message_topic,message_payload):
    sql = """
    INSERT INTO test_log(topic,payload,status) VALUES(%s,%s,%s)
    """%(message_topic,message_payload,"MQTT代码服务器已收到")
    sql_need_roll(sql)

insert_data(message_topic,message_payload)
'''
