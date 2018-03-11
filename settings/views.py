from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from settings.models import Profile


# TODO Make authentication required
def user_settings(request, uuid):
    context = {}
    # If the user is requesting his/her own user settings page
    if request.user.profile.uuid == uuid:
        context['first_name'] = request.user.first_name
        context['last_name'] = request.user.last_name
        context['username'] = request.user.username
    # Must be a staff user to access someone else's settings page\
    elif request.user.is_staff:
        # Query all User and Profile fields for the given Profile UUID
        user = User.objects.filter(profile__uuid=uuid) \
            .select_related('profile')[0]
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['username'] = user.username
    return render(request, 'settings/user_settings.html', context)

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