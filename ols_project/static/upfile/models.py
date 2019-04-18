from django.db import models

class User_info_table(models.Model):#用户信息表
    class Meta():
        db_table = 'user_info_table'
    user_num = models.AutoField(primary_key=True)#用户序列编号（自动增长主键）
    phone_num = models.CharField(max_length=11)#手机号
    prepaid_wallet = models.DecimalField(max_digits=7,decimal_places=2)#充值钱包 max=99999.99
    red_packet = models.DecimalField(max_digits=6,decimal_places=2)#红包 max=9999.99
    register_time = models.DateField(auto_now_add=True)#注册时间（在生成用户的时候自动添加，无需管理）
    user_type = models.CharField(max_length=3)#用户类型（用户、管理员、投资商、维保员）
    last_login_time = models.DateTimeField(auto_now=True)#最后登录时间（最后一次修改时间，暂时不知道SELECT和UPDATE）
    security_num = models.CharField(max_length=6)#验证码

class Garage_info_table(models.Model):#库机信息表
    class Meta():
        db_table = 'garage_info_table'
    garage_num = models.AutoField(primary_key=True)#库机序列编号(主键)
    investor_num = models.CharField(max_length=20)#投资商编号
    garage_code = models.CharField(max_length=14)#库机编码（如：GDS100001）
    pub_code = models.CharField(max_length=14)#MQTT发布主题码（如：C/gds100001/S）
    garage_name = models.CharField(max_length=15)#库机名称（如：仲恺后街充电库机）
    longitude = models.DecimalField(max_digits=13,decimal_places=10)#经度
    latitude = models.DecimalField(max_digits=12,decimal_places=10)#纬度
    address = models.CharField(max_length=30)#地址
    operation_state = models.CharField(max_length=3)#运营状态（运营中、维护中）
    running_state = models.CharField(max_length=20)#车库运行状态
    door_state = models.CharField(max_length=8)#库门开关状态（L0.M1.R0）

class Parking_financial_table(models.Model):#车位财务表
    class Meta():
        db_table = 'parking_financial_table'
    financial_num = models.AutoField(primary_key=True)#财务表序列编号(主键)
    garage_num = models.ForeignKey('Garage_info_table',on_delete=models.CASCADE)#库机序列编号（库机信息表的外键）
    user_num = models.ForeignKey('User_info_table',on_delete=models.CASCADE)#用户序列编号（用户信息表的外键）
    parking_num = models.IntegerField()#车位号
    parking_start_time = models.DateTimeField()#停车开始时间
    charge_wattage = models.DecimalField(max_digits=5,decimal_places=2)#充电瓦数
    charge_cost = models.DecimalField(max_digits=5,decimal_places=2)#充电计费
    parking_cost = models.DecimalField(max_digits=5,decimal_places=2)#停车计费
    total_price = models.DecimalField(max_digits=5,decimal_places=2)#总价格
    parking_end_time = models.DateTimeField()#停车结束时间

class Garage_exception_table(models.Model):#库机异常报表
    class Meta():
        db_table = 'garage_exception_table'
    path_num = models.AutoField(primary_key=True)#报表序列编号（主键）
    garage_num = models.ForeignKey('Garage_info_table',on_delete=models.CASCADE)#库机序列编号（库机信息表的外键）
    user_num = models.ForeignKey('User_info_table',on_delete=models.CASCADE)#用户序列编号（用户信息表的外键）
    exception_type = models.CharField(max_length=20)#异常类型（1#2#5#6#）
    exception_description = models.CharField(max_length=200)#异常描述(200字内)
    report_time = models.DateTimeField(auto_now_add=True)#报告时间（无需管理）

class Upload_file_table(models.Model):#上传文件表
    class Meta():
        db_table = 'upload_file_table'
    path_num = models.ForeignKey('Garage_exception_table',on_delete=models.CASCADE)#报表序列编号
    path = models.CharField(max_length=50)#路径

class Garage_parking_state_table(models.Model):#库机车位状态表
    class Meta():
        db_table = 'upload_file_table'
    garage_num = models.ForeignKey('Garage_exception_table',primary_key=True,on_delete=models.CASCADE)#库机序列编号（主键外键）
    parking_num = models.IntegerField(primary_key=True)#车位号（主键）
    exist_car = models.BooleanField()#是否有车
    parking_start_time = models.DateTimeField(blanke=True)#开始停车时间
    charge_wattage = models.DecimalField(max_digits=5,decimal_places=2)#充电瓦数
    charge_state = models.BooleanField()#充电状态

class Recharge_record_table(models.Model):#充值记录表
    class Meta():
        db_table = 'recharge_record_table'
    user_num = models.ForeignKey('User_info_table',on_delete=models.CASCADE)#用户序列编号（外键）
    recharge_num = models.DecimalField(max_digits=3,decimal_places=0)#充值数额
    red_packet = models.DecimalField(max_digits=3,decimal_places=0)#赠送红包
    recharge_time = models.DateTimeField(auto_now_add=True)#充值时间
