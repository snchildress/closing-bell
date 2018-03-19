from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from settings.models import Profile

from datetime import date, datetime


# External view
@login_required
def request_vacation(request):
    """
    Renders a page to request vacation time and displays
    previous and future requests
    """
    if request.method == 'POST':
        data = request.POST
        start_date = data['start-date']
        end_date = data['end-date']
        profile = request.user.profile
        reduce_days(profile, start_date, end_date)

    return render(request, 'scheduler/home.html')


# Internal helper functions
def accrue_days():
    """
    Adds monthly accrual days to all users who have not yet
    accrued days in the current month
    """
    # Get the current month in ISO format
    today = date.today()
    current_month = today.strftime('%Y-%m-01T00:00:00.000Z')

    # Get profiles that have not been updated yet this month
    profiles = Profile.objects.filter(update_timestamp__lt=current_month)

    for profile in profiles:
        # Get the monthly accrual days and max allowable accrual days
        monthly_accrual_days = profile.annual_accrual_days / 12
        max_allowable_accrual_days = profile.max_allowable_accrual_days

        # Add the monthly accrual days to the remaining accrual days
        profile.remaining_accrual_days += monthly_accrual_days

        # If the remaining accrual days exceeds the max, set it to the max
        if profile.remaining_accrual_days > max_allowable_accrual_days:
            profile.remaining_accrual_days = max_allowable_accrual_days

        profile.save()

def reduce_days(profile, start_date, end_date):
    """
    Reduces a user's remaining accrual balance by the number of
    vacation days requested
    """
    # Convert dates to datetime formats
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Get difference between dates in days
    number_of_days_requested = end_date - start_date
    number_of_days_requested = number_of_days_requested.days

    # Reduce the user's remaining accrual days by the number of days requested
    profile.remaining_accrual_days -= number_of_days_requested
    profile.save()
