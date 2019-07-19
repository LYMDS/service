import smtplib
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
def send_Email(code):
    '''
        login()方法用来登录SMTP服务器，sendmail()方法就是发邮件，由于可以一次发给多个人，所以传入一个list，邮件正文
        是一个str，as_string()把MIMEText对象变成str。
    '''
    #构造纯文本邮件内容
    msg = MIMEText('验证码：%s'%code,'plain','utf-8')
    msg['Subject'] = Header('LYMDS验证码', 'utf-8')
    msg['From'] = 'lym_ds@163.com'  
    msg['To'] = "609586869@qq.com"
    #发送者邮箱
    sender = 'lym_ds@163.com'
    #发送者的登陆用户名和密码
    user = 'lym_ds@163.com'
    password = 'lymds1'
    #发送者邮箱的SMTP服务器地址
    smtpserver = 'smtp.163.com'
    #接收者的邮箱地址
    #receiver = ['609586869@qq.com',user] #receiver 可以是一个list
    receiver = '609586869@qq.com'
    smtp = smtplib.SMTP() #实例化SMTP对象
    smtp.connect(smtpserver,25) #（缺省）默认端口是25 也可以根据服务器进行设定
    smtp.login(user,password) #登陆smtp服务器
    smtp.sendmail(sender,receiver,msg.as_string()) #发送邮件 ，这里有三个参数
    smtp.quit()
    return code
if __name__ == "__main__":
    code = "875930"
    a = send_Email(code)
    print(a)