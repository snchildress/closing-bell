from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

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
        success = reduce_days(profile, start_date, end_date)
        if success:
            # Get clean formats for the month, day, and year
            start_date_year = start_date[0:4]
            start_date_month = start_date[5:7]
            start_date_day = start_date[8:10]
            end_date_year = end_date[0:4]
            end_date_month = end_date[5:7]
            end_date_day = end_date[8:10]
            # If only one day was requested, message success for that day
            if start_date == end_date:
                messages.success(request, 'Your vacation request for ' + \
                    start_date_month + '/' + start_date_day + '/' + \
                start_date_year + ' was successfully submitted!')
            # Otherwise message success for both dates provided
            else:
                messages.success(request, 'Your vacation request for ' + \
                    start_date_month + '/' + start_date_day + '/' + \
                    start_date_year + ' to ' + end_date_month + '/' + \
                    end_date_day + '/' + end_date_year + ' was \
                    successfully submitted!')
        else:
            messages.error(request, 'Oops! There was an issue processing \
                your request.')

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
    try:
        # Convert dates to datetime formats
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Get difference between dates in days, adding 1 to include both dates
        number_of_days_requested = end_date - start_date
        number_of_days_requested = number_of_days_requested.days + 1

        # Reduce the user's remaining accrual days by the number of days requested
        profile.remaining_accrual_days -= number_of_days_requested
        profile.save()
        return True
    
    except Exception as e:
        print(e)
        return False
