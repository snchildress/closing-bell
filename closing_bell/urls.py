from django.contrib import admin
from django.conf import settings
from django.urls import include, path

from . import views

import importlib

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout', views.logout_auth),
]

for app in settings.CUSTOM_APPS:
    urlpatterns.append(path(app + '/', include(importlib.import_module(app + '.urls'))))
