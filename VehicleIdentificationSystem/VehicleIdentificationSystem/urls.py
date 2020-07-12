"""VehicleIdentificationSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
'''
author: 郑志强
create time: 2020/7/10
update time: 2020/7/12
'''
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('online-identification/', views.online_identification, name='online-identification'),
    path('download-packages/', views.download_packages, name='download-packages'),
    path('download-doc/',views.download_doc, name='download-doc'),
    path('online-identification/model/', views.online_identification_model, name='online-identification/model'),
    path('online-identification/license/', views.online_identification_license, name='online-identification/license'),
    path('online-identification/nums/', views.online_identification_nums, name='online-identification/nums'),
    path('online-identification/attributes/', views.online_identification_attributes, name='online-identification/attributes'),
    path('online-identification/destroy/', views.online_identification_destroy, name='online-identification/destroy'),
    path('online-identification/drive', views.online_identification_drive, name='online-identification/drive'),
]
