from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class user_registration(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=150, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField()  
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_email_notification = models.BooleanField(default=False)
    reward_points = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'user_registration'

# Custom function to set the initial value
@receiver(pre_save, sender=user_registration)
def set_initial_user_id(sender, instance, **kwargs):
    if not instance.pk:
        # Only set the user_id if it's a new record
        max_id = user_registration.objects.aggregate(max_id=models.Max('user_id'))['max_id']
        if max_id is None:
            instance.user_id = 10000
        else:
            instance.user_id = max_id + 1