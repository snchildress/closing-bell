from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


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
    start_date = instance.start_date
    end_date = instance.end_date

    # Get difference between dates in days, adding 1 to include both dates
    number_of_days_requested = end_date - start_date
    number_of_days_requested = number_of_days_requested.days + 1
    instance.number_of_days = number_of_days_requested
