from django.db import models

# Create your models here.
class Test_log(models.Model):
    topic = models.CharField(max_length=30,default="0")
    payload = models.CharField(max_length=30,default="0")
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    class Meta():
        db_table = 'test_log'
