import requests
import json
url = "http://127.0.0.1:8000/mqtt_receive"
headers = {'Content-Type': 'text/plain;charset=UTF-8',
           #'Connection': 'Keep-Alive',
           'Cache-Control':'no-cache'}
def send_to_django(data):
    requests.get(url,headers=headers,params=data)

'''
url = "http://127.0"
json_data = json.loads(r.text)
print("状态码：",r.status_code)
print("内容：",json_data["all"][1][0])
print(type(r))
print(type(json_data))
'''