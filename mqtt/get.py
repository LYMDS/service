import requests
import json
import time
headers = {'Content-Type': 'text/plain;charset=UTF-8',
           #'Connection': 'Keep-Alive',
           'Cache-Control':'no-cache'}

url='http://172.17.37.63:8000/information?user_num=1'
r=requests.get(url,headers=headers)
json_data = json.loads(r.text)
print("状态码：",r.status_code)
print("内容：",json_data["all"][1][0])
print(type(r))
print(type(json_data))

