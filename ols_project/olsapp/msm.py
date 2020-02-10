import requests
import xml.etree.ElementTree as ET
def send2Phone(mobile_num,random_code):
    data = {
        'method'  : 'sendMsg',
        'username': 'JSM42941',
        'password': 'mp5xq56d',
        'veryCode': 'pc16u79mchp3',
        'mobile'  : mobile_num,
        'tempid'  : 'JSM42941-0001',
        'content' : '@1@=%s'%random_code,
        'msgtype' : '2',
        'code'    : 'utf-8'
    }
    url = "http://112.74.76.186:8030/service/httpService/httpInterface.do"
    response = requests.post(url=url, data=data)
    content = {}
    root = ET.fromstring(response.text)
    content[root[0][0].tag] = root[0][0].text
    content[root[0][1].tag] = root[0][1].text
    return content        # 返回{""""}
    
if __name__ == "__main__":
    msm('17324080646','456321')
