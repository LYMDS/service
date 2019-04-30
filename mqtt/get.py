import requests
import json

headers = {'Content-Type': 'text/plain;charset=UTF-8',
           #'Connection': 'Keep-Alive',
           'Cache-Control':'no-cache'}
url='http://www.olswxapp.top/information?user_num=1'

r=requests.get(url,headers=headers)
print("状态码：",r.status_code)
json_data = json.loads(r.text)
print("内容：",json_data["all"][1][0])

print("++++++++++++++++++++++++++++++++++++")
print(type(r))
print(type(json_data))
