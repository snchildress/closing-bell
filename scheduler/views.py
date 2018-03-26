from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum

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
                start_date_year + ' was successfully scheduled!')

            # Otherwise message success for both dates provided
            else:
                messages.success(request, 'Your vacation request for ' + \
                    start_date_month + '/' + start_date_day + '/' + \
                    start_date_year + ' - ' + end_date_month + '/' + \
                    end_date_day + '/' + end_date_year + ' was \
                    successfully scheduled!')
        
        # Otherwise message that an error occurred
        except Exception as e:
            print(e)
            messages.error(request, 'Oops! There was an issue processing \
                your request.')


    # Get relevant dates in ISO format for queries
    today = date.today()
    current_date = today.strftime('%Y-%m-%dT00:00:00.000Z')
    current_year = today.strftime('%Y-01-01T00:00:00.000Z')

    # Get all of the user's requests
    requests = Request.objects.filter(user=request.user)
    # Sort past requests in descending order
    past_requests = requests.filter(end_date__lte=current_date)\
        .order_by('-end_date')
    # Sort future requests in ascending order
    future_requests = requests.filter(start_date__gt=current_date)\
        .order_by('start_date')
    # Get the number of days requested YTD
    requested_days_ytd = requests.filter(start_date__gt=current_year)\
        .aggregate(total=Sum('number_of_days'))['total']

    # Sum the number of days requested before and after today
    past_requests_ytd = past_requests.aggregate(total=Sum('number_of_days'))['total']
    future_requests_ytd = future_requests.aggregate(total=Sum('number_of_days'))['total']

    # Get the user's profile
    profile = Profile.objects.get(user__id=request.user.id)

    # Calculate number of days accrued YTD using the annual accrual day policy
    days_accrued_ytd = today.month / 12 * float(profile.annual_accrual_days)

    # Get the lifetime number of days accrued to compare to days accrued YTD
    lifetime_days_accrued = profile.remaining_accrual_days
    if requested_days_ytd:
        lifetime_days_accrued += requested_days_ytd
    
    # If user began accruing mid-current year
    if lifetime_days_accrued < days_accrued_ytd:
        days_accrued_ytd = lifetime_days_accrued

    context = {
        'past_requests': past_requests,
        'future_requests': future_requests,
        'past_requests_ytd': past_requests_ytd,
        'future_requests_ytd': future_requests_ytd,
        'profile': profile,
        'days_accrued_ytd': days_accrued_ytd,
    }

    return render(request, 'scheduler/home.html', context)

@login_required
def delete_request(request, request_id):
    """
    Deletes the given request if the request belongs to the
    requesting user
    """
    try:
        # Query the request from the given request ID
        request_to_delete = Request.objects.get(id=request_id)

        # Do not allow non-staff users to delete other users' requests
        if not request.user.is_staff and request_to_delete.user != request.user:
            messages.error(request, 'You cannot delete requests belonging to \
                other users!')
            return redirect('home')

        # Get the request start and end dates for clear messaging
        start_date = str(request_to_delete.start_date)
        end_date = str(request_to_delete.end_date)

        # Get clean formats for the month, day, and year of request dates
        start_date_year = start_date[0:4]
        start_date_month = start_date[5:7]
        start_date_day = start_date[8:10]
        end_date_year = end_date[0:4]
        end_date_month = end_date[5:7]
        end_date_day = end_date[8:10]
    
        # Otherwise delete the request and message accordingly
        request_to_delete.delete()
        if start_date == end_date:
            messages.success(request, 'Your request for ' + start_date_month \
                + '/' + start_date_day + '/' + start_date_year + \
                ' was successfully deleted!')
        else:
            messages.success(request, 'Your request for ' + start_date_month \
                + '/' + start_date_day + '/' + start_date_year + ' - ' \
                + end_date_month + '/' + end_date_day + '/' + end_date_year \
                + ' was successfully deleted!')

    except Exception as e:
        print(e)
        messages.error(request, 'It looks like that request no longer exists!')

    return redirect('home')


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
