from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render


# Authentication views
def login_auth(request):
    """
    Serves a login page to authenticate users or logs the user in
    """
    # Redirect authenticated users back to the user's settings page
    if request.user.is_authenticated:
        return redirect('user_settings', request.user.profile.uuid)

    # If user is not submitting credentials, show login page
    if request.method != 'POST':
        return render(request, 'authentication/login.html')

    # Get the submitted username and password to authenticate the credentials
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    # If credentials were successful, log the user in
    if user:
        login(request, user)
        # Redirect the user back to previously visited page
        next_page = request.POST.get('next', 'all_users_settings')
        return redirect(next_page)

    # Message that invalid credentials were given
    else:
        messages.error(request, 'Invalid username or password.')
        context = {'username': username}
        return render(request, 'authentication/login.html', context)

def logout_auth(request):
    """
    Log the current user out
    """
    logout(request)
    return redirect('login')
