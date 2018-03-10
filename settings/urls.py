from django.urls import path
from . import views


urlpatterns = [
    path('user/<int:id>', views.user_settings),
    path('users/all', views.all_users_settings),
]
