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
    power = request.GET.get('Power')
    voltage = request.GET.get('Voltage')
    print(iface, csid , pno , qty , state, stamp, stime, power, voltage)
    which_gar = Garage_info_table.objects.get(garage_code = csid)#用发过来的csid车库号去与车位号找该车库Key来解，没通过则返回错误
    gar_num = which_gar.garage_num
    which_side = Garage_parking_state_table.objects.filter(garage_num=gar_num,parking_num=ascii_to_garint(pno))
    key = which_side.charge_key
    my_str = iface + key + csid + pno + qty + state + stamp + stime
    new_str = hashlib.md5(my_str.encode()).hexdigest().upper()
    if new_str == hash_str:
        # mqtt发布工作，本需核对车库类型（算法兼容可以不核对分流）
        state_list = ["Sc0"]
        gar_list = Garage_parking_state_table.objects.filter(garage_num=gar_num).order_by('parking_num')
        for i in gar_list:
            if i.charge_state in (0, 1):
                state_list.append('0')
            elif i.charge_state in (2, 3):
                state_list.append('b')
        state_list.append('T')
        send_msg = "".join(state_list)
        mqtt_publish(which_gar.pub_code,send_msg)
        print('\n接口名称：%s\n充电桩的key：%s\n车库编号：%s\n车位号：%s\n电量：%s\n状态：%s\n时间戳：%s\n充电开始时间：%s'%(iface,key,csid,pno,qty,state,stamp,stime))
        qty = float(qty)/10
        state = int(state)
        zeroc = which_side.exist_car
        if zeroc:
            zeroc = "0"
        else:
            zeroc = "1"
        which_side.charge_state = state
        which_side.charge_wattage = qty
        which_side.charge_power = float(power)
        which_side.charge_voltage = float(voltage)
        which_side.save()
        control_tuple=(state,which_side.control_state)
        if control_tuple == (0,None) or control_tuple == (1,None) or control_tuple == (2,None) or control_tuple == (3,None) or control_tuple == (1,1):
            return JsonResponse({'rcode':0,'cmd':0,'rmsg':'ok','zeroc':zeroc})
        if control_tuple == (0,0) or control_tuple == (2,0) or control_tuple == (3,0) or control_tuple == (1,0):
            return JsonResponse({'rcode':0,'cmd':1,'rmsg':'ok','zeroc':zeroc})
        if control_tuple == (0,1) or control_tuple == (2,1) or control_tuple == (3,1):
            return JsonResponse({'rcode':0,'cmd':2,'rmsg':'ok','zeroc':zeroc})
    print(csid,pno,"该充电桩KEY未通过")
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

import numpy as np
def status2list(status):
    dic = {
            'a':[[2, 2, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [0, 2, 2],
                 [2, 1, 2]],
            'b':[[2, 2, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 2, 0],
                 [2, 1, 2]],
            'c':[[2, 2, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [0, 2, 2],
                 [2, 0, 2],
                 [2, 1, 2]],
            'd':[[2, 2, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 2, 0],
                 [2, 0, 2],
                 [2, 1, 2]],
            'e':[[2, 2, 2],
                 [2, 0, 2],
                 [0, 2, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 1, 2]],
            'f':[[2, 2, 2],
                 [2, 0, 2],
                 [2, 2, 0],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 1, 2]],
            'g':[[2, 2, 2],
                 [0, 2, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 1, 2]],
            'h':[[2, 2, 2],
                 [2, 2, 0],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 1, 2]],
            'i':[[2, 2, 2],
                 [0, 2, 2],
                 [0, 2, 2],
                 [0, 2, 2],
                 [0, 2, 2],
                 [1, 2, 2]],
            'j':[[2, 2, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 0, 2],
                 [2, 1, 2]],
            'k':[[2, 2, 2],
                 [2, 2, 0],
                 [2, 2, 0],
                 [2, 2, 0],
                 [2, 2, 0],
                 [2, 2, 1]]
    }
    return dic[status]


def ascii_dirft_num(char):
    return ord(char) - 97
def dirft(olist,i):#该算法不允许溢出左右移位，溢出则是原数组
    return olist[-i:]+olist[:-i]
def subscript(n,RL):
    def section(n,i,or_so):
        if i == 1:
            index0 = np.arange(n,0,-i)
        else:
            index0 = np.arange(0,n,-i)
        index1 = np.full(n,1+or_so*i)
        index1[0] = 1
        return np.column_stack((index0,index1))
    upper_part = section(n,1,RL)
    lower_part = section(n,-1,RL)
    res = np.vstack((upper_part,lower_part))
    return res.tolist()
    
def garage_msg(request): # 前端需求的显示控制码
    which_gar = request.GET.get("garage_code")
    garage = Garage_info_table.objects.get(garage_code = which_gar)
    park_msg = Garage_parking_state_table.objects.filter(garage_num=garage).order_by("parking_num")
    status = garage.side_control  # 拿出控制码
    if garage.garage_type == 0: # 升降横移
        control = status2list(status)   # 升降横移的专用显示转换
        print(control)
        ready_load = []
        for i in park_msg:
            load = [i.parking_num, i.exist_car, i.charge_state, i.lock_state, i.car_id]     # 模拟车牌号先
            ready_load.append(load)
        #该算法需要自底而上，从左至右遇到2填装数据
        m = 0
        for i in range(5,-1,-1):
            for j in range(3):
                if control[i][j] == 2:
                    control[i][j] = ready_load[m]
                    m+=1
    elif garage.garage_type == 1: # 垂直循环车库的显示转换算法,基本可以通用
        n = int(park_msg.count()/2)
        con_list = subscript(n,1)#状态 'a' 时的填装下标，其他的都是相对于本列表来移位
        dirft_num = ascii_dirft_num(status)
        con_list = dirft(con_list,dirft_num)#取对应的循环移位控制码
        control = np.zeros((n+1,3),dtype=int).tolist()
        k = 0
        for i in park_msg:
            load = [i.parking_num, i.exist_car, i.charge_state, i.lock_state, i.car_id]
            index = con_list[k]
            control[index[0]][index[1]] = load
            k+=1
    return JsonResponse({"gar_msg": control})

def garage_msg1(request): # 前端需求的显示控制码
    which_gar = request.GET.get("garage_code")
    garage = Garage_info_table.objects.get(garage_code = which_gar)
    park_msg = Garage_parking_state_table.objects.filter(garage_num=garage).order_by("parking_num")
    status = garage.side_control  # 拿出控制码
    if garage.garage_type == 0: # 升降横移
        control = status2list(status)   # 升降横移的专用显示转换
        print(control)
        ready_load = []
        for i in park_msg:
            load = [i.parking_num, i.exist_car, i.charge_state, i.lock_state, i.car_id]     # 模拟车牌号先
            ready_load.append(load)
        # ready_load = sorted(ready_load,key=itemgetter(0))#为什么要在这里排序
        m = 0
        for i in range(0,18):#对数值为2的填装数据
            if control[i] == 2:
                control[i] = ready_load[m]
                m+=1
    elif garage.garage_type == 1: # 垂直循环车库的显示转换算法
        con_list = [4, 6, 9, 12, 16, 14, 11, 8]#状态 'a' 时的填装下标，其他的都是相对于本列表来移位
        dirft_num = ascii_dirft_num(status)
        con_list = dirft(con_list,dirft_num)#取对应的循环移位控制码
        control = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        k = 0
        for i in park_msg:
            load = [i.parking_num, i.exist_car, i.charge_state, i.lock_state, i.car_id]
            control[con_list[k]] = load
            k+=1
    return JsonResponse({"gar_msg": control})

    
from django.http import FileResponse
def download(request):#传送图片给客户端的方法
    file = open('./static/upfile/10.png','rb')
    response = FileResponse(file)
    response['Content-Type']='application/octet-stream'
    #response['Content-Disposition']='attachment;filename="你的图片.png"'
    return response

import os
import re
import base64
def base64_to_img(base64_str,file_name):#Base64特殊图片保存算法
    base64_str = re.sub("(-)", "+", base64_str)
    base64_str = re.sub("(_)", "/", base64_str)
    base64_str = re.sub("(\.)", "=", base64_str)
    with open("./static/upfile/%s.jpg"%file_name, "wb") as f:
        f.write(base64.b64decode(base64_str))

# def decipher_side(side_code,door_state):
#     m = 0
#     for i in door_state:
#         if i == "1":
#             for j in range(0,16,3):
#                 k = m + j
#                 if side_code[k] == 2:
#                     return side_code[0:k+1].count(2)
#         m += 1

def decipher_side(side_code,door_state):#升降横移的位状态转译算法
    alist = np.array(side_code)
    shape = alist.shape
    height = shape[0]
    width  = shape[1]
    for i in range(width):
        if door_state[i] == '1':
            for j in range(height-2,-1,-1):
                if alist[j,i] == 2:
                    break
            break
    side_num = 0
    for m in range(height-1,-1,-1):
        if m != j:
            side_num += side_code[m].count(2)
        else:
            side_num += side_code[m][0:i+1].count(2)
            break
    return side_num

@csrf_exempt   
def camera_post(request):
    Type = request.POST['type']                 #是否在线传输 online/offline
    plate_num = request.POST['plate_num']       #车牌号码
    plate_color = request.POST['plate_color']   #车牌颜色
    car_logo = request.POST['car_logo']         #车辆品牌
    car_color = request.POST['car_color']       #车辆颜色
    vehicle_type = request.POST['vehicle_type'] #车辆类型       
    start_time = request.POST['start_time']     #车牌识别时间,1970/01/01 到现在的秒数目
    park_id = request.POST['park_id']           #车库ID 最大支持 60 个字符 
    cam_id = request.POST['cam_id']             #相机ID 相机ID号根据配置决定是使用MAC还是UID
    picture = request.POST['picture']           #全景图，BASE64编码为避免Http传输时URL编码意外改变图片的BASE64编码，作了特殊的替换：'+'替换为'-'，'/'替换为'_'，'='替换为'.'
    closeup_pic = request.POST['closeup_pic']   #每张车牌的特写照
    print(Type, plate_num, plate_color, car_logo, car_color, vehicle_type, start_time, park_id, cam_id)

    garage = Garage_info_table.objects.get(garage_code=park_id)

    if garage.garage_type == 0:
        state = status2list(garage.side_control)                #返回前端控制的数组
        parking_side = decipher_side(state,garage.door_state)   #返回一个车位号
    elif garage.garage_type == 1:
        parking_side = ord(garage.side_control) - 96

    which_side = Garage_parking_state_table.objects.get(garage_num=garage.garage_num,
                                                        parking_num=parking_side)  # 找出那个车位
    if which_side.exist_car == 0:
        which_side.car_id = plate_num
        which_side.car_logo = car_logo
        which_side.car_color = plate_color
        which_side.car_type = vehicle_type
        which_side.save()
        base64_to_img(picture, park_id)
        base64_to_img(closeup_pic, park_id + str(parking_side))
    return JsonResponse({'s':'sdsada'})


def pay_algorithm(tspan,wattage):#财务算法
    #一分钟一毛钱先，红包可以抵扣10%
    #一瓦电两元
    charge_cost = wattage*2
    parked_cost = tspan/10
    total = charge_cost + parked_cost
    red = total/10
    wallet = total - red
    return [wallet, red, charge_cost, parked_cost, total]#分别为：钱包、红包、充电花费、停车花费、总金额

def mqtt_to_django(request):
    garage = request.GET.get('garage')#直接就是主键
    garage_type = request.GET.get('garage_type')#类型
    runing_state = request.GET.get('running_state')#车库运行状态，直接存起来
    have = request.GET.get('exist_car')#车位的有无车状态
    door = request.GET.get('door_state')#门状态，直接存起来
    control = request.GET.get("side_control")#前端显示的控制态
    which_gar = Garage_info_table.objects.get(garage_num=garage)
    which_gar.running_state = runing_state
    which_gar.door_state = door
    which_gar.side_control = control
    which_gar.save()
    side = which_gar.garage_parking_state_table_set.all().order_by('parking_num')
    for i in range(side.count()):
        write_data = Garage_parking_state_table.objects.filter(state_num=side[i].state_num)

        if side[i].exist_car == int(have[i]):
            continue

        elif side[i].exist_car == 0 and have[i] == '1':#车停好
            write_data.update(exist_car=1,parking_start_time=datetime.datetime.now())

        elif side[i].exist_car == 1 and have[i] == '0':#车开走
            start_time = side[i].parking_start_time
            howlong = time_span(start_time).minutes
            wattage = side[i].charge_wattage
            pay = pay_algorithm(howlong,wattage)
            payer = User_info_table.objects.get(user_num=side[i].user_num)
            payer.prepaid_wallet -= pay[0]
            payer.red_packet -= pay[1]
            payer.save()
            financial_data = Parking_financial_table()
            financial_data.garage_num = which_gar
            financial_data.user_num = payer
            financial_data.parking_num = side[i].parking_num
            financial_data.parking_start_time = start_time
            financial_data.charge_wattage = wattage
            financial_data.charge_cost = pay[2]
            financial_data.parking_cost = pay[3]
            financial_data.total_price = pay[4]
            financial_data.parking_end_time = datetime.datetime.now()
            financial_data.red_packet_expense = pay[1]
            financial_data.save()
            write_data.update(exist_car=0,
                              parking_start_time=None,
                              car_id='无车牌',
                              car_logo='未知',
                              car_color='未知',
                              car_type='未知',
                              charge_wattage=0,
                              charge_power=0,
                              charge_voltage=0)
    return JsonResponse({"code":"ok"})

"""
预约算法暂时停用，因为与不能远程遥控的安全逻辑冲突！
def dsad(request):
    car_num = request.GET['car_plate']
    gar_code = request.GET['car_plate']
    which_gar = Garage_info_table.objects.get(garage_code=gar_code)
    side_list = Garage_parking_state_table.objects.filter(garage_num=which_gar,exist_car=0)
    nops = side_list.count()
    key_list = cache.keys(gar_code+"-*")
    if nops - len(key_list) < 2:
        return JsonResponse("最后一位不能预约")#可以细分情况
    elif not side_list.exists():
        return JsonResponse("存满了呦！客官")
    #通过上面两个过滤，现在为客户预约
    key = ''
    for i in range(1,51):
        test_key = gar_code+"-%d"%i
        if test_key not in key_list:
            key = test_key
            break
    cache.set(key,gar_code,timeout=30*60)
    return JsonResponse("预约成功")
"""


#用户余额查询
def balance_over(request):
    user = request.GET.get("user_num")
    user = User_info_table.objects.get(user_num = user)
    return JsonResponse({
        "money": user.prepaid_wallet,
        "red_packet": user.red_packet #讨论是否做成一体化
    })
    

import requests
import random
def determine_money(request):
    user_num = request.GET.get('user_num')
    spbill_create_ip = request.META['REMOTE_ADDR'] #拿到终端ip
    appid = "wx1f4d8f20fadf2d8e"
    secret = "65fc833b87550d97525f6250914eebcc"
    code = request.GET.get("code")
    authorization_code = "authorization_code"
    openid_url = "https://api.weixin.qq.com/sns/jscode2session?appid="+appid+"&secret="+secret+"&js_code="+code+"&grant_type="+authorization_code
    res = requests.get(openid_url)
    openid = res.json()['openid'] #拿到openid  数据库要加字段！！！！！！还没加！！！勿删！！！
    session_key = res.json()['session_key'] #拿到会话密钥 鬼知道什么时候用到
    out_trade_no = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    nonce_str = ""
    for i in range(0,12):
        out_trade_no += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-|*')
    for i in range(0,32):
        nonce_str += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    ret = {
        "appid": appid,
        "body": '撒打算',#body,      #商品描述 传入中文
        "mch_id": '3457689wse',#mch_id,  #商户号 还没拿到
        "nonce_str": nonce_str,  #随机字符串 上面生成了
        "notify_url": 'w242e',#notify_url,  #通知地址 即是微信服务器通知支付结果的地址 我们可能不需要 自己做查询
        "openid": openid, #上面拿到了直接用
        "out_trade_no": out_trade_no,  #上面生成了直接传
        "spbill_create_ip": spbill_create_ip,  #终端IP 上面拿到了
        "total_fee": '20.13',#total_fee, #订单总金额 取到分 拿钱拿钱拿钱拿钱还没做
        "trade_type": 'JSAPI' #交易类型 小程序支付默认为该值
    };
    Mch_key = "241242add" #商户密钥信息未拿到 快点申请公司注册商户搞定？？？
    stringA = '&'.join(["{0}={1}".format(k, ret.get(k))for k in sorted(ret)])
    stringSignTemp = '{0}&key={1}'.format(stringA,Mch_key)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    sign = sign.upper() #第一次签名完成
    bodyData = '<xml>'     #开始封装xml                                      
    bodyData += '<appid>' + ret['appid'] + '</appid>'              #小程序ID
    bodyData += '<body>' + ret['body'] + '</body>'                        #商品描述
    bodyData += '<mch_id>' + ret['mch_id'] + '</mch_id>'                  #商户号
    bodyData += '<nonce_str>' + ret['nonce_str'] + '</nonce_str>'         #随机字符串
    bodyData += '<notify_url>' + ret['notify_url'] + '</notify_url>'      #支付成功的回调地址
    bodyData += '<openid>' + ret['openid'] + '</openid>'                  #用户标识
    bodyData += '<out_trade_no>' + ret['out_trade_no'] + '</out_trade_no>'#商户订单号
    bodyData += '<spbill_create_ip>' + ret['spbill_create_ip'] + '</spbill_create_ip>'#客户端终端IP
    bodyData += '<total_fee>' + ret['total_fee'] + '</total_fee>'         #总金额 单位为分
    bodyData += '<trade_type>JSAPI</trade_type>'                   #交易类型 小程序取值如下：JSAPI
    bodyData += '<sign>' + sign + '</sign>'
    bodyData += '</xml>'   #封装xml完成
    orders_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder' #微信统一下单的api 需要服务器去请求
    respone = requests.post(orders_url,bodyData.encode("utf-8"),headers={'Content-Type': 'application/xml'}) 
    print(respone.text)
    return JsonResponse({'s':'a'})


#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
def reg_investor(request):
    cookies = request.COOKIES
    print(cookies)
    render(request,'reg.html',{'session_id': cookies})
















