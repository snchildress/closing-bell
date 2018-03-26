from django.urls import path
from . import views

urlpatterns = [
    path('', views.request_vacation, name='request_vacation'),
    path('<uuid:uuid>', views.request_vacation, name='user_requests'),
    path('delete/request/<int:request_id>', views.delete_request, name='delete_request'),
]
