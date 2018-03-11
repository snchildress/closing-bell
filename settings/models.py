from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField('User UUID', default=uuid.uuid4)
    remaining_accrual_days = models.DecimalField(max_digits=4,
                                                 decimal_places=2)
    annual_accrual_days = models.DecimalField(max_digits=4,
                                              decimal_places=2)
    max_allowable_accrual_days = models.IntegerField()
    create_timestamp = models.DateTimeField('Creation Date',
                                            auto_now_add=True)
    update_timestamp = models.DateTimeField('Last Updated Date',
                                            auto_now=True)

    def __str__(self):
        return str(self.user) + ' User Profile'

    class Meta:
        db_table = 'user_profiles'
        verbose_name_plural = 'User Profiles'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a Profile record when creating new User records
    """
    if created:
        try:
            Profile.objects.create(user=instance)
        except Exception as e:
            print(e)
            pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the corresponding Profile record when saving a User record
    """
    try:
        instance.profile.save()
    except Exception as e:
        print(e)
        pass
