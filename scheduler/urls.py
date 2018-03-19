from django.urls import path
from . import views

urlpatterns = [
    path('', views.request_vacation, name='request_vacation'),
]
