'''
author: 郑志强
create time: 2020/7/22
update time: 2020/7/22
'''
from django.urls import path
from . import views

app_name = 'driveractions'

urlpatterns = [
    path('result/', views.get_license_result),
]