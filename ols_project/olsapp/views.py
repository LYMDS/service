from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache

import datetime
def time_span(old_time):
    timespan = datetime.datetime.now()-old_time
    #timespan = datetime.datetime.now()-old_time.replace(tzinfo=None)
    #old_time = old_time.split(".")[0]
    #timespan = datetime.datetime.now()-datetime.datetime.strptime(old_time,'%Y-%m-%d %H:%M:%S')
    return timespan

import random
def gain_code():
    code=""
    for i in range(0,6):
        code+=random.choice('1234567890')
    return code

from .models import User_info_table
def getCode(request):

    phone = request.GET['phone']
    print(phone)
    code = gain_code()
    try:
        old_user = User_info_table.objects.get(phone_num = phone)
        print("用户已注册")
        old_user.security_num = code
        old_user.save()
    except User_info_table.DoesNotExist:
        print("找不到该用户")
        user = User_info_table()
        user.phone_num = phone
        user.prepaid_wallet = 0.00
        user.red_packet = 90.00
        user.user_type = "用户"
        user.security_num = code
        user.save()
    out = {"code":code}
    return JsonResponse(out)


def login(request):
    phone = request.GET["phone"]
    code = request.GET["code"]
    user = User_info_table.objects.get(phone_num = phone)
    overtime = "0"
    check = "0"
    if time_span(user.last_login_time).seconds > 60:
        overtime = "1"
    if user.security_num == code:
        check = '1'
    out = {
        "check":check,
        "user_num":user.user_num,
        "overtime":overtime
    }
    return JsonResponse(out)
	
	
def check_time(request):
    num = request.GET["user_num"]
    user = User_info_table.objects.get(user_num = num)
    overtime = "0"
    if time_span(user.last_login_time).days > 60:
        overtime = "1"
    out = {"overtime":overtime}
    return JsonResponse(out)


from .models import Garage_info_table,Garage_parking_state_table
def map_init(request):
    garage = Garage_info_table.objects.all()
    out = []
    for i in garage:
        empty = Garage_parking_state_table.objects.filter(garage_num = i.garage_num)
        empty_num = 0
        for j in empty:
            if j.exist_car == 0:
                empty_num+=1
        dic={
                'garage_code' : i.garage_code,
                'garage_name' : i.garage_name,
                'longitude' : float(i.longitude),
                'latitude' : float(i.latitude),
                'address' : i.address,
                'empty' : empty_num
            }
        out.append(dic)
    return JsonResponse({'garage_info':out})

def ascii_to_garint(char):
    return ord(char) - 64
import paho.mqtt.publish as pub
def mqtt_publish(topic,context):
    pub.single(topic,context,
               hostname="localhost",
               qos=2,
               retain=False,
               port=1883,
               auth={"username":"olswxmqtt","password":"olswxappmqtt32219"})
               
import hashlib
def charge_msg(request):
    
    iface = request.GET.get('iface')
    csid = request.GET.get('csid')
    pno = request.GET.get('pno')
    qty = request.GET.get('qty')
    state = request.GET.get('state')
    stamp = request.GET.get('stamp')
    stime = request.GET.get('stime')
    hash_str = request.GET.get('hash')
    #更新的充电桩信息
    power = request.GET.get('Power')#充电桩的功率
    voltage = request.GET.get('Voltage')#充电桩的电压
    print(iface,csid , pno , qty , state, stamp, stime)
    
    #用发过来的csid车库号去与车位号找该车库Key来解，没通过则返回错误
    which_gar = Garage_info_table.objects.get(garage_code = csid).garage_num
    which_side = Garage_parking_state_table.objects.filter(garage_num=which_gar,parking_num=ascii_to_garint(pno))
    key = which_side.charge_key
    my_str = iface + key + csid + pno + qty + state + stamp + stime
    new_str = hashlib.md5(my_str.encode()).hexdigest().upper()
    if new_str == hash_str:
        print('\n接口名称：%s\n充电桩的key：%s\n车库编号：%s\n车位号：%s\n电量：%s\n状态：%s\n时间戳：%s\n充电开始时间：%s'%(iface,key,csid,pno,qty,state,stamp,stime))
        qty = float(qty)/10
        state = int(state)
        print(qty,"    ",state)
        zeroc = which_side.exist_car
        if zeroc:
            zeroc = "0"
        else:
            zeroc = "1"
        which_side.charge_state = state
        which_side.charge_wattage = qty
        which_side.save()
        control_tuple=(state,which_side.control_state)
        if control_tuple == (0,None) or control_tuple == (1,None) or control_tuple == (2,None) or control_tuple == (3,None) or control_tuple == (1,1):
            return JsonResponse({'rcode':0,'cmd':0,'rmsg':'ok','zeroc':zeroc})
        if control_tuple == (0,0) or control_tuple == (2,0) or control_tuple == (3,0) or control_tuple == (1,0):
            return JsonResponse({'rcode':0,'cmd':1,'rmsg':'ok','zeroc':zeroc})
        if control_tuple == (0,1) or control_tuple == (2,1) or control_tuple == (3,1):
            return JsonResponse({'rcode':0,'cmd':2,'rmsg':'ok','zeroc':zeroc})
    
    
    #mqtt发布工作
    gar_list = Garage_parking_state_table.objects.filter(garage_num=which_gar).order_by('id')
    state_list = ["Sc0"]
    for i in gar_list:
        if i.charge_state in (0,1):
            state_list.append('0')
        elif i.charge_state in (2,3):
            state_list.append('1')
    state_list.append('T')
    send_msg = "".join(state_list)
    mqtt_publish(which_side.charge_key,send_msg)
    return JsonResponse({'rcode':101,'cmd':0,'rmsg':'unknown error'})
	
from .models import Garage_exception_table
def exception(request):
    which_user = request.GET.get('user_num')
    which_garage = request.GET.get('garage_code')
    report_type = request.GET.get('type')
    report_text = request.GET.get('report')
    date_time = request.GET.get('date_time')
    exist = 1
    try:
        garage = Garage_info_table.objects.get(garage_code = which_garage)
        user = User_info_table.objects.get(user_num = which_user)
        report_table = Garage_exception_table()
        report_table.garage_num = garage
        report_table.user_num = user
        report_table.exception_type = report_type
        report_table.exception_description = report_text
        report_table.report_time = date_time
        report_table.save()
    except:
        exist = 0
        nowtime = "error"
        print('有错误-------------------------------')
	
    return JsonResponse({
        'exist':exist,
        'nowtime':date_time
    })



import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt#引入csrf验证装饰器
from .models import Upload_file_table
@csrf_exempt
def upload(request):
    date_time0 = request.POST.get('datetime')
    #date_time = ":".join((date_time,"000000"))
    date_time = datetime.datetime.strptime(date_time0,'%Y-%m-%d %H:%M:%S')
    which_user = request.POST.get('user_num')
    img_num = request.POST.get('img_num')
    user = User_info_table.objects.get(user_num = which_user)
    path_num= Garage_exception_table.objects.get(report_time__exact=date_time,user_num=user)#user_num=user,"2019-04-10 18:19:13"
    if request.method=="POST":
        f = request.FILES["file"]
        filename = ".".join(("_".join(( which_user , date_time0 , img_num )),f.name.rsplit(".",1)[1]))
        upload_table = Upload_file_table()
        upload_table.path_num = path_num
        upload_table.path = filename
        upload_table.save()
        filePath = os.path.join(settings.MDEIA_ROOT,filename)
        print(filePath)
        with open(filePath,"wb") as fp:
            for info in f.chunks():
                fp.write(info)
    return JsonResponse({
        "state" : "ok"
    })
	

def show_charge(request):
    g = Garage_parking_state_table.objects.get(state_num = 53)
    zero = "不清零"
    state = "错误状态"
    if g.charge_state == 0:
        state = "待机状态"
    elif g.charge_state == 1:
        state = "故障状态"
    elif g.charge_state == 2:
        state = "正在充电"
    elif g.charge_state == 3:
        state = "充满状态"
    if g.control_state == 0:
        control = '停止充电'
    elif g.control_state == 1:
        control = '开始充电'
    elif g.control_state == None:
        control = '不控制'
    if g.exist_car == 0:
        zero = '清零'
    return render(request,'charge_test.html',{'wallage':g.charge_wattage,'charge_state':state,'control_state':control,'zero':zero})

from django.shortcuts import redirect
@csrf_exempt
def write_state(request):
    control = request.POST.get('control')
    print("------------------------------------------------------")
    print("改变了状态：",control)
    print("------------------------------------------------------")
    g = Garage_parking_state_table.objects.get(state_num = 53)
    g.control_state = int(control)
    g.save()
    return redirect("/charge_test")


from operator import itemgetter
from .models import Parking_financial_table
from .models import Recharge_record_table,Garage_info_table
def information(request):
    which_user = request.GET.get('user_num')
    try:
        user = User_info_table.objects.get(user_num = which_user).user_num
        parking_financials = Parking_financial_table.objects.filter(user_num = user)#所有消费表 车位财务表
        records = Recharge_record_table.objects.filter(user_num=user) #所有充值表
        count1 = parking_financials.count()
        count2 = records.count()
        count = count1+count2
        llist = []
        end_list = []
        for i in range(0,count1):
            parking_time = parking_financials[i].parking_end_time-parking_financials[i].parking_start_time
            #智能化显示时长后期算法处理预留parking_time.days seconds microseconds milliseconds minutes hours weeks
            pktime = parking_time.seconds
            garagename=parking_financials[i].garage_num.garage_name #Django查询子表时若子表里有外键，则该外键对象是其主表的对象（所以此处是可以直接拿Garage_info_table里的garage_name）
            ttuple = (parking_financials[i].parking_end_time,
                      parking_financials[i].charge_cost,
                      parking_financials[i].parking_cost,
                      parking_financials[i].total_price,
                      garagename,
                      pktime)
            llist.append(ttuple)
        for j in range(0,count2):
            ttuple2 = (records[j].recharge_time,records[j].recharge_num,records[j].red_packet)
            llist.append(ttuple2)
        end_list = sorted(llist,key=itemgetter(0),reverse=True)	
    except:
        print('有错误-------------------------------')
    return JsonResponse({
        'all':end_list
    })

def status2list(status):
    dic = {'a':[2,1,2,0,2,2,2,0,2,2,0,2,2],
           'b':[2,1,2,2,2,0,2,0,2,2,0,2,2],
           'c':[2,1,2,2,0,2,0,2,2,2,0,2,2],
           'd':[2,1,2,2,0,2,2,2,0,2,0,2,2],
           'e':[2,1,2,2,0,2,2,0,2,0,2,2,2],
           'f':[2,1,2,2,0,2,2,0,2,2,2,0,2],
           'g':[2,1,2,2,0,2,2,0,2,2,0,2,0],
           'h':[2,1,2,2,0,2,2,0,2,2,0,2,2],
           'i':[1,2,2,0,2,2,0,2,2,0,2,2,0],
           'j':[2,1,2,2,0,2,2,0,2,2,0,2,2],
           'k':[2,2,1,2,2,0,2,2,0,2,2,0,2]}
    return dic[status]
    
def garage_msg(request):
    print("ssadsadasasdsadsadsdsadsa")
    which_gar = request.GET.get("garage_code")
    garage = Garage_info_table.objects.get(garage_code = which_gar)
    status = garage.running_state#解出控制码
    control = status2list("1")#先不拿数据库的，模拟一下
    print(control)
    park_msg = Garage_parking_state_table.objects.filter(garage_num = garage)
    ready_load = []
    for i in park_msg:
        load = [i.parking_num, i.exist_car, i.charge_state, i.lock_state, "粤M 68595"]#模拟车牌号先
        ready_load.append(load)
    ready_load = sorted(ready_load,key=itemgetter(0))
    m = 0
    for i in range(0,18):
        if control[i] == 2:
            control[i] = ready_load[m]
            m+=1
    return JsonResponse({"gar_msg": control})
    
from django.http import FileResponse
def download(request):
    file = open('./static/upfile/10.png','rb')
    response = FileResponse(file)
    response['Content-Type']='application/octet-stream'
    #response['Content-Disposition']='attachment;filename="你的图片.png"'
    return response

@csrf_exempt   
def carid(request):
    path = request.POST['car_plate']
    color = request.POST['color']
    Type = request.POST['type']
    park_id = request.POST['park_id']
    camera_id = request.POST['camera_id']
    start_time = request.POST['start_time']
    method = request.method
    print(path,method,color,Type,park_id,start_time,camera_id)  
    return JsonResponse("{'s':'sdsada'}",safe = False)

    

#仿真：客户预约触发函数,需要挑选车库出来
def dsad(request):
    car_num = request.GET['car_plate']
    gar_code = request.GET['car_plate']
    which_gar = Garage_info_table.objects.get(garage_code=gar_code)
    side_list = Garage_parking_state_table.objects.filter(garage_num=which_gar,exist_car=0)
    if side_list.count() == 1:
        return JsonResponse("最后一位不能预约")
    elif !side_list.exists():
        return JsonResponse("已经预约满了")
    key_list = cache.keys(which_gar)
    
"""
"""
























