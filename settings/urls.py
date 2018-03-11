from django.urls import include, path
from . import views

user_patterns = [
    path('<int:id>', views.user_settings),
    path('new', views.create_new_user),
]

urlpatterns = [
    path('user/', include(user_patterns)),
    path('users/all', views.all_users_settings),
]
