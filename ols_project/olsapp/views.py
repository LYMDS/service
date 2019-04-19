from django.shortcuts import render
from django.http import JsonResponse


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


import hashlib
def charge_msg(request):
	iface = request.GET.get('iface')
	csid = request.GET.get('csid')
	pno = request.GET.get('pno')
	qty = float(request.GET.get('qty'))
	state = int(request.GET.get('state'))
	stamp = request.GET.get('stamp')
	stime = request.GET.get('stime')
	hash_str = request.GET.get('hash')
	print(iface,csid , pno , qty , state, stamp, stime)
	key=['gfegfdgfdgdfgdgg','dfgfdgfdgfdgfdg','WECSD8SDSDSDADWWE','gfegfdgfdgjjgdfg']
	add = csid + pno + qty + state + stamp + stime
	for i in key:
		my_str = iface + i + add
		new_str = hashlib.md5(my_str.encode()).hexdigest().upper()
		if new_str == hash_str:
			print('\n接口名称：%s\n充电桩的key：%s\n车库编号：%s\n车位号：%s\n电量：%s\n状态：%s\n时间戳：%s\n充电开始时间：%s'%(iface,i,csid,pno,qty,state,stamp,stime))
			which_gar = Garage_parking_state_table.objects.get(state_num = 1)
			which_gar.charge_state = state
			which_gar.charge_wattage += qty
			which_gar.save()
			if state == 0 and which_gar.control_state == 1:
				#读取控制态
				which_gar.control_state = None
				which_gar.save()
				return JsonResponse({'rcode':0,'cmd':2,'rmsg':'ok'})
			if state == 1 and which_gar.control_state == 0:
				return JsonResponse({'rcode':0,'cmd':1,'rmsg':'ok'})
			if state in (3,4) or state == 0 and which_gar.control_state in (0,None) or state == 0 and which_gar.control_state in (None,1):
				return JsonResponse({'rcode':0,'cmd':0,'rmsg':'ok'})
			break
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
	g = Garage_parking_state_table.objects.get(state_num = 1)
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
	return render(request,'charge_test.html',{'wallage':g.charge_wattage,'charge_state':state,'control_state':control})

from django.shortcuts import redirect
@csrf_exempt
def write_state(request):
	control = request.POST.get('control')
	print(type(control))
	g = Garage_parking_state_table.objects.get(state_num = 1)
	g.control_state = int(control)
	g.save()
	return redirect("/charge_test")



from .models import Parking_financial_table
from .models import Recharge_record_table
def information(request):
	which_user = request.GET.get('user_num')
	which_garage = request.GET.get('garage_code')
	try:
		user = User_info_table.objects.get(user_num = which_user).user_num
		garage = Garage_info_table.objects.get(garage_num = which_garage).garage_num
		print(user)
		print(garage)
		garage_name = Garage_info_table.objects.get(garage_num = garage).garage_name
		print(garage_name)
		parking_financials=Parking_financial_table.objects.filter(garage_num = garage,user_num = user).order_by("-parking_end_time")#所有消费表 车位财务表
		records=Recharge_record_table.objects.filter(user_num=user).order_by("-recharge_time") #所有充值表
		count1=parking_financials.count()
		count2=records.count()
		count=count1+count2
		if (count1<=count2):
			for index in range(count1):
				for index2 in range(count2):
					if (parking_financials[index].parking_end_time>records[index2].recharge_time):
						print(1)
						break
					elif:
						#shunxupailie
					
						
			
		

		
	except:
		print('有错误-------------------------------')
	return JsonResponse({
		#'all_record':llist[0],
		#'garage_name':garage_name,
		#'total_price':total_price,
		#'charge_cost':charge_cost,
		#'parking_cost':parking_cost,
		#'red_packet_expense':red_packet_expense,
		'parking_time':count
	})


























