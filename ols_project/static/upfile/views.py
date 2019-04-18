from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import random

def code():
	code=""
	for i in range(0,6):
		code+=random.choice('1234567890')
	return code

from .models import User_info_table
def getCode(request):
	phone = request.POST.get('phone')
	code = code()
	user = User_info_table()
	try:
		data = User_info_table.objects.get(phone_num = phone)
		print("用户已注册")
	except DoesNotExist:
		print("找不到该用户")
		user.phone_num = phone
		user.prepaid_wallet = 0
		user.red_packet = 90
		user.user_type = "用户"
	finally:
		user.security_num = code
		user.save()
	out = {
		"code":code
	}
	return JsonResponse(out)
	


	

	
	
	
	
