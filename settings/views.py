from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User


def user_settings(request, id):
    return render(request, 'settings/user_settings.html')

def create_new_user(request):
    context = {'new_user': True}

    if request.method == 'GET':
        return render(request, 'settings/user_settings.html', context)

    else:
        try:
            # Get form field submissions
            data = request.POST
            first_name = data['first-name']
            last_name = data['last-name']
            username = data['username']
            password = data['password']
            annual_accrual_days = data['annual-accrual-days']
            max_allowable_accrual_days = data['max-allowable-accrual-days']

            # Create user object
            user = User.objects.create_user(username, username, password)
            user.first_name = first_name
            user.last_name = last_name
            user.profile.annual_accrual_days = annual_accrual_days
            user.profile.max_allowable_accrual_days = max_allowable_accrual_days
            user.profile.remaining_accrual_days = 0
            user.save()

        except Exception as e:
            print(e)

        return render(request, 'settings/user_settings.html', context)

def all_users_settings(request):
    return render(request, 'settings/all_users_settings.html')