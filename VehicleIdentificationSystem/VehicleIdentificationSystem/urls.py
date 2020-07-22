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
create time: 2020/7/13
update time: 2020/7/19
'''
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/license/', include('license.api.urls', namespace='license')),
    path('api/nums/', include('nums.api.urls', namespace='nums')),
    path('api/carmodels/', include('carmodels.api.urls', namespace='carmodels')),
    path('api/driveractions/', include('driveractions.api.urls', namespace='driveractions')),
]
