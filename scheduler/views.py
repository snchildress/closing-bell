from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from settings.models import Profile
from scheduler.models import Request

from datetime import date, datetime


# External view
@login_required
def request_vacation(request):
    """
    Renders a page to request vacation time and displays
    previous and future requests
    """
    # Accrue monthly days for each user who hasn't yet accrued this month
    accrue_days()

    if request.method == 'POST':
        try:
            # Get request dates and convert to ISO format
            data = request.POST
            start_date = data['start-date'] + 'T00:00:00.000Z'
            end_date = data['end-date'] + 'T00:00:00.000Z'

            # Create a Request record with the given dates
            request_record = Request.objects.create(
                user=request.user,
                start_date=start_date,
                end_date=end_date
            )

            # Get clean formats for the month, day, and year of request dates
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
        
        # Otherwise message that an error occurred
        except Exception as e:
            print(e)
            messages.error(request, 'Oops! There was an issue processing \
                your request.')


    # Get the current date in ISO format
    today = date.today()
    current_date = today.strftime('%Y-%m-%dT00:00:00.000Z')

    # Get all of the user's requests
    requests = Request.objects.filter(user=request.user)
    # Sort past requests in descending order
    past_requests = requests.filter(end_date__lte=current_date)\
        .order_by('-end_date')
    # Sort future requests in ascending order
    future_requests = requests.filter(start_date__gt=current_date)\
        .order_by('start_date')
    context = {
        'past_requests': past_requests,
        'future_requests': future_requests,
    }

    return render(request, 'scheduler/home.html', context)


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