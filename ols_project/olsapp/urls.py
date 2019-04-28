"""ols_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^getCode/$',views.getCode),
    url(r'^login/$',views.login),
    url(r'^onLaunch/$',views.check_time),
    url(r'^map_init/$',views.map_init),
    url(r'^charge_msg/$',views.charge_msg),
    url(r'^exception/$',views.exception),
    url(r'^except_upload/$',views.upload),	
    url(r'^charge_test/$',views.show_charge),#测试视图
    url(r'^charge_t/$',views.write_state),
    url(r'^information/$',views.information),
    url(r'^garage_msg/$',views.garage_msg),
<<<<<<< HEAD
    url(r'^show_img/$',views.download),
=======
>>>>>>> 1d005a26c04ac00223826f6f831d349e981c4183
]
