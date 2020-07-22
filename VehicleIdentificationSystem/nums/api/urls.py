from django.urls import path
from . import views

app_name = 'nums'

urlpatterns = [
    path('result/', views.get_license_result)
]