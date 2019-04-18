import hashlib as HaSh
import time
import random
'WECSD8SDSDSDADWWE'
def get_key():
    code = ''
    for i in range(0,17):
        code+=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    return code

start = time.time()
iface = "rptState"
csid  = "gds100001"
pno   = "C"
qty   = "1123"
state = "1"
stamp = "1488335833"
stime = "1488335500"
add = csid + pno + qty + state + stamp + stime
recode = '4BE5EBDE63EE38374D02A372EAB353D2'

for i in range(0,1000):
    key   = get_key()
    hash_str = iface + key + add
    new = HaSh.md5(hash_str.encode()).hexdigest()
    

end = time.time()
print(end - start)
