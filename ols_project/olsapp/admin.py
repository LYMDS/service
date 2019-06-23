from django.contrib import admin

# Register your models here.
from .models import User_info_table
@admin.register(User_info_table)
class User_info_tableAdmin(admin.ModelAdmin):
    pass
