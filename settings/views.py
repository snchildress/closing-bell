from django.http import HttpResponse
from django.shortcuts import render


def user_settings(request, id):
    return render(request, 'settings/user_settings.html')

def create_new_user(request):
    context = {'new_user': True}

    if request.method == 'GET':
        return render(request, 'settings/user_settings.html', context)

    else:
        data = request.POST
        first_name = data['first-name']
        last_name = data['last-name']
        username = data['username']
        password = data['password']
        annual_accrual_days = data['annual-accrual-days']
        max_allowable_accrual_days = data['max-allowable-accrual-days']
        return render(request, 'settings/user_settings.html', context)

def all_users_settings(request):
    return render(request, 'settings/all_users_settings.html')