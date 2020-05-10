from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from .models import *
import os
import paho.mqtt.publish as pub
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt#引入csrf验证装饰器
import datetime

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
# Create your views here.
def send_message(request):
    topic = request.POST.get('topic')
    payload = request.POST.get('payload')
    #publish
    send(topic,payload)
    #publish
    logws = Test_log()
    logws.status = '发布成功'
    logws.topic = topic
    logws.payload = payload
    logws.save()
    log = Test_log.objects.all()
    return render(request,'test.html',{'logfile':log})

def show(request):
    log = Test_log.objects.all()
    return render(request,'test.html',{'logfile':log})


@csrf_exempt
def savefile(request):
	if request.method=="POST":
		f = request.FILES["file"]
		filePath = os.path.join(settings.MDEIA_ROOT,f.name)
		with open(filePath,"wb") as fp:
			for info in f.chunks():
				fp.write(info)
	return render(request,'upload.html')

def showsave(request):
	return render(request,'upload.html')

def connect(request):
    return JsonResponse({"name":"我是你爸爸","type":123.2321})

def hb_connect(request):
    weight = request.GET.get('weight')
    data = HB_Hardware()
    data.weight = float(weight)
    data.time_now = datetime.datetime.now() + datetime.timedelta(hours=16)
    data.save()
    return JsonResponse({"status":"ok"})

def hb_show(request):
    hardware = HB_Hardware.objects.all().order_by("-time_now")
    return JsonResponse({'data': hardware})

















