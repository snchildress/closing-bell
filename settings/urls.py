from django.urls import path
from . import views


urlpatterns = [
    path('user/<int:id>', views.display_user_settings),
    path('users/all', views.display_all_users_settings),
]
