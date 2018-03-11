from django.contrib.auth import logout
from django.shortcuts import redirect


# Authentication views
def logout_auth(request):
    logout(request)
    return redirect('admin/logout/')
