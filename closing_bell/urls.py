from django.contrib import admin
from django.conf import settings
from django.urls import include, path

import importlib

urlpatterns = [
    path('admin/', admin.site.urls)
]

for app in settings.CUSTOM_APPS:
    urlpatterns.append(path(app + '/', include(importlib.import_module(app + '.urls'))))
