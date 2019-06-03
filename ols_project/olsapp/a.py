import os,re,base64


with open("img","r") as f:
    base64_str = f.read()
print(base64_str[0:100])
base64_str = re.sub("(-)","+",base64_str)
base64_str = re.sub("(_)","/",base64_str)
base64_str = re.sub("(\.)","=",base64_str)
print(base64_str[0:100])
with open("a.jpg","wb") as f:
    f.write(base64.b64decode(base64_str))

