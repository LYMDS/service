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
    url(r'^investor_reg/$',views.investor_reg),#不要加到头上来
    url(r'^getCode/$',views.getCode),
    url(r'^login/$',views.login),
    url(r'^onLaunch/$',views.check_time),
    url(r'^map_init/$',views.map_init),
    url(r'^charge_msg/$',views.charge_msg),
    url(r'^exception/$',views.exception),
    url(r'^except_upload/$',views.upload),	
    url(r'^charge_test/$',views.show_charge),
    url(r'^charge_t/$',views.write_state),
    url(r'^information/$',views.information),
    url(r'^garage_msg/$',views.garage_msg),
    url(r'^show_img/$',views.download),
    url(r'^camera_post/$',views.camera_post),
    url(r'^mqtt_receive/$',views.mqtt_to_django),
    url(r'^balance_over/$',views.balance_over),
    url(r'^determine_money/$',views.determine_money),
    url(r'^reg_investor/$',views.reg_investor),
    url(r'^admin_login$',views.admin_login),
    url(r'^ajax/$', views.ajax),
    


]
