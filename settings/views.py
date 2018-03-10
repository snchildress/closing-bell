from django.http import HttpResponse
from django.shortcuts import render


def user_settings(request, id):
    return render(request, 'settings/user_settings.html')

def all_users_settings(request):
    return render(request, 'settings/all_users_settings.html')