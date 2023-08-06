from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index),
    path('post/ip/', views.post_esp_ip),
    path('get/ip/', views.get_esp_ip)
]
