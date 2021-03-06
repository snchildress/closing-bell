from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from datetime import datetime


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_days = models.DecimalField(max_digits=4, decimal_places=2)
    start_date = models.DateTimeField('Request Start Date')
    end_date = models.DateTimeField('Request End Date')
    create_timestamp = models.DateTimeField('Creation Date',
                                            auto_now_add=True)
    update_timestamp = models.DateTimeField('Last Updated Date',
                                            auto_now=True)
    
    def __str__(self):
        return self.user.first_name + ' ' + \
            self.user.last_name + ' (' + str(self.start_date) + ')'

    class Meta:
        db_table = 'requests'
        verbose_name_plural = 'Vacation Requests'

@receiver(pre_save, sender=Request)
def number_of_days(sender, instance, **kwargs):
    """
    Uses the start and end dates to save the Request record's
    number of days requested
    """
    # Get the record's start and end dates
    start_date = datetime.strptime(instance.start_date, '%Y-%m-%dT00:00:00.000Z')
    end_date = datetime.strptime(instance.end_date, '%Y-%m-%dT00:00:00.000Z')

    # Get difference between dates in days, adding 1 to include both dates
    number_of_days_requested = end_date - start_date
    number_of_days_requested = number_of_days_requested.days + 1
    instance.number_of_days = number_of_days_requested

@receiver(post_save, sender=Request)
def decrease_remaining_accrual_days(sender, instance, created, **kwargs):
    """
    Decreaes a User's remaning accrual balance by the requested amount
    of vacation days after a Request record is created
    """
    if created:
        # Reduce the User's remaining balance by the requested amount
        profile = instance.user.profile
        profile.remaining_accrual_days -= instance.number_of_days
        profile.save()

@receiver(pre_delete, sender=Request)
def increase_remaining_accrual_days(sender, instance, **kwargs):
    """
    Increases a User's remaining accrual balance by the requested amount
    of vacation days before deleting that Request record
    """
    profile = instance.user.profile
    profile.remaining_accrual_days += instance.number_of_days
    profile.save()
