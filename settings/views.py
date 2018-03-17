from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    update_session_auth_hash,
    login
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from settings.models import Profile


# External views
@login_required
def user_settings(request, uuid):
    if request.method == 'POST':
        try:
            # Get form field submissions
            data = request.POST
            first_name = data['first-name']
            last_name = data['last-name']
            username = data['username']
            password = data['new-password']

            user = authenticate(request, username=username,
                                password=password)
            if user is not None:
                # Update the user's session and authenticate again
                user.set_password(password)
                update_session_auth_hash(request, user)
                login(request, user)
                # Use the new user settings to update the database record
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.save()

        except Exception as e:
            print(e)
            pass

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

@login_required
def create_new_user(request):
    # Must be a staff user to create a new user
    if not request.user.is_staff:
        return redirect('user_settings', request.user.profile.uuid)

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

            # Create User and Profile records
            user = User.objects.create_user(username, username, password)
            user.first_name = first_name
            user.last_name = last_name
            user.profile.annual_accrual_days = annual_accrual_days
            user.profile.max_allowable_accrual_days = \
                max_allowable_accrual_days
            user.save()

        except Exception as e:
            print(e)
            pass

        return redirect('all_users_settings')

@login_required
def all_users_settings(request):
    # Must be a staff user to view all users' settings
    if not request.user.is_staff:
        return redirect('user_settings', request.user.profile.uuid)

    if request.method == 'POST':
        try:
            data = request.POST
            uuid = data['profile-uuid']
            first_name = data['first-name']
            last_name = data['last-name']
            annual_accrual_days = data['annual-accrual-days']
            max_allowable_accrual_days = data['max-allowable-accrual-days']

            # Query all User and Profile fields for the given Profile UUID
            user = User.objects.filter(profile__uuid=uuid) \
                .select_related('profile')[0]
            user.first_name = first_name
            user.last_name = last_name
            user.profile.annual_accrual_days = annual_accrual_days
            user.profile.max_allowable_accrual_days = \
                max_allowable_accrual_days
            user.save()
        
        except Exception as e:
            print(e)
            pass

    # Query all User and Profile records
    users = User.objects.all().select_related('profile')
    context = {'users': users}
    return render(request, 'settings/all_users_settings.html', context)

@login_required
def delete_user(request, uuid):
    # Must be a staff user to delete users
    if not request.user.is_staff:
        return redirect('user_settings', request.user.profile.uuid)

    try:
        user = User.objects.get(profile__uuid=uuid)
        user.delete()

    except Exception as e:
        print(e)
        pass

    return redirect('all_users_settings')
