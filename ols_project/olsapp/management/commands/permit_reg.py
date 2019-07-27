from django.core.management import BaseCommand
from django.contrib.sessions.backends.db import SessionStore
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('session_id',help="指定name字段")  # name 必须参数，输入的第一个参数的值将赋值给name，必须参数
        parser.add_argument('-s','--set',help="指定telephone字段",type=bool)   # 可选参数 -t 或 --telephone -t是简写形式。
    
    def handle(self, *args, **options):
        default = True
        if options['set'] != None and options['set'] == False:
            default = False
        s = SessionStore(session_key = options['session_id'])
        s["admin_permission"] = default
        s.save()
        print("授权%s成功"%default)
