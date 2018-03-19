from django.contrib import admin
from django.conf import settings
from django.urls import include, path

from . import views

import importlib

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login_auth, name='login'),
    path('logout', views.logout_auth, name='logout'),
]

for app in settings.CUSTOM_APPS:
    urlpatterns.append(path(app + '/', include(importlib.import_module(app + '.urls'))))

# Set the root path to the scheduler's request vacation page
from scheduler.views import request_vacation

urlpatterns.append(path('', request_vacation, name='home'))
