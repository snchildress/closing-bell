from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    update_session_auth_hash,
    login
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test
)
from django.contrib import messages

from settings.models import Profile


# Internal helper
def is_staff(user):
    """
    Validates that a user is authenticated with staff access
    """
    return user.is_staff


# External views
@login_required
def user_settings(request, uuid):
    """
    Displays or edits a user's settings
    """
    # Non-staff users can only access their own settings
    if not request.user.is_staff:
        uuid = request.user.profile.uuid

    own_settings = True
    if request.user.is_staff and uuid != request.user.profile.uuid:
        own_settings = False

    # Query all User and Profile fields for the given Profile UUID
    user = User.objects.filter(profile__uuid=uuid) \
        .select_related('profile')[0]

    if request.method == 'POST':
        try:
            # Get form field submissions
            data = request.POST
            first_name = data['first-name']
            last_name = data['last-name']
            username = data['username']
            new_password = data['new-password']

            # Verify the user's password to allow for user record changes if own settings
            if own_settings:
                password = data['password']
                user = authenticate(request, username=user.username,
                                    password=password)

            # User must be authenticated or editing someone else's settings to edit
            if user:
                # Update the user's session and authenticate again
                if new_password:
                    user.set_password(new_password)

                    # Reauthenticate to avoid being signed out
                    if own_settings:
                        update_session_auth_hash(request, user)
                        login(request, user)
                    messages.success(request, 'Password successfully updated.')

                # Use the new user settings to update the database record
                if user.first_name != first_name \
                        or user.last_name != last_name \
                        or user.username != username:
                    # If there's a new username, update it
                    if user.username != username:
                        user.username = username
                        user.email = username
                        messages.success(request, 'Username successfully updated.')

                    # If there's a new first or last name, update it
                    if user.first_name != first_name or user.last_name != last_name:
                        user.first_name = first_name
                        user.last_name = last_name
                        messages.success(request, 'Name successfully updated.')

                # Otherwise message that no updates were requested
                elif not new_password:
                    messages.warning(request, 'You didn\'t request any updates.')
                user.save()
            else:
                messages.error(request, 'Invalid password!')

        except Exception as e:
            print(e)
            messages.error(request, 'Oops! Something went wrong.')

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'own_settings': own_settings,
    }
    return render(request, 'settings/user_settings.html', context)

@user_passes_test(is_staff)
def create_new_user(request):
    """
    Creates a new user in the system
    """
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

            # Create new User record
            try:
                user = User.objects.create_user(username, username, password)
            except Exception as e:
                print(e)
                messages.error(request, username + ' already exists!')
                return redirect('new_user')

            # Add additional User and Profile record data
            user.first_name = first_name
            user.last_name = last_name
            user.profile.annual_accrual_days = annual_accrual_days
            user.profile.max_allowable_accrual_days = \
                max_allowable_accrual_days
            user.save()

        except Exception as e:
            print(e)
            messages.error(request, 'Oops! There was an issue creating that user.')
            return redirect('new_user')

        return redirect('all_users_settings')

@user_passes_test(is_staff)
def all_users_settings(request):
    """
    Displays and allows for edits to all users in the system
    """
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
            messages.success(request, first_name + '\'s settings \
                successfully updated!')
        
        except Exception as e:
            print(e)
            messages.error(request, 'Oops! There was an issue updating ' \
                + first_name + '\'s settings.')

    # Query all User and Profile records
    users = User.objects.all().select_related('profile')
    context = {'users': users}
    return render(request, 'settings/all_users_settings.html', context)

@user_passes_test(is_staff)
def delete_user(request, uuid):
    """
    Permanently deletes a user
    """
    try:
        user = User.objects.get(profile__uuid=uuid)
        first_name = user.first_name
        last_name = user.last_name
        user.delete()
        messages.success(request, first_name + ' ' + last_name + ' was \
            successfully deleted.')

    except Exception as e:
        print(e)
        messages.error(request, 'There was an issue deleting that user.')

    return redirect('all_users_settings')
