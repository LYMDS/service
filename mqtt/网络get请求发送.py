import requests
import time
i = 0
client=requests.session()
headers = {'Content-Type': 'text/plain;charset=UTF-8',
           #'Connection': 'Keep-Alive',
           'Cache-Control':'no-cache'}
url='http://120.77.156.184:80/charge_msg/?iface=rptState&csid=gds100001&pno=C&qty=1123&state=1&stamp=1488335833&stime=1488335500&hash=4BE5EBDE63EE38374D02A372EAB353D2'

for i in range(0,1000):
    r=client.get(url,headers=headers)
    print(r.status_code)
