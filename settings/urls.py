from django.urls import include, path
from . import views

user_patterns = [
    path('<uuid:uuid>', views.user_settings, name='user_settings'),
    path('new', views.create_new_user, name='new_user'),
    path('delete/<uuid:uuid>', views.delete_user, name='delete_user'),
]

urlpatterns = [
    path('user/', include(user_patterns)),
    path('users/all', views.all_users_settings, name='all_users_settings'),
]
