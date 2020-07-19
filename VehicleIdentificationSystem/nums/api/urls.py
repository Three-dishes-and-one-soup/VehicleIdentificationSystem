'''
author: 郑志强
create time: 2020/7/15
update time: 2020/7/15
'''
from django.urls import path
from . import views

app_name = 'nums'

urlpatterns = [
    path('result/', views.get_license_result)
]