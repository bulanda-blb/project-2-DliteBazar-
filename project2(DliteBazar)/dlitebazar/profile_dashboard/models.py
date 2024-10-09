from django.db import models
from user_registration.models import user_registration  
from django.db.models.signals import pre_save
from django.dispatch import receiver

class upload_images(models.Model):
    image_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='uploaded_images/')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    keywords = models.TextField()
    
    # Extra fields generated in views
    size = models.PositiveIntegerField()  # size in kb
    resolution = models.CharField(max_length=50)  # e.g., '1920x1080'
    file_format = models.CharField(max_length=20)
    dpi = models.PositiveIntegerField()
    uploaded_datetime = models.DateTimeField()
    sold_multiple_counter = models.PositiveIntegerField()
    liked_by_counter = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'uploaded_images'



class liked_images(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    image = models.ForeignKey('upload_images', on_delete=models.CASCADE)
    liked_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'image')
        db_table = 'liked_images'



class purchased_items(models.Model):
    email = models.EmailField()
    address = models.TextField()
    phone = models.IntegerField()
    payment_method = models.CharField(max_length=50)
    terms_accepted = models.BooleanField(default=True)
    image = models.ForeignKey('upload_images', on_delete=models.CASCADE)
    purchased_by = models.ForeignKey(user_registration, on_delete=models.CASCADE, related_name='purchased_by')
    purchase_from = models.ForeignKey(user_registration, on_delete=models.CASCADE, related_name='purchased_from')
    purchase_date = models.DateTimeField()
    payment_success = models.BooleanField()
    max_download = models.IntegerField(default=10)
    downloaded_count = models.IntegerField(default=0)
    discounted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'purchased_items'


class contact_us(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        db_table = 'contact_us'


class support_ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('progress', 'In Progress'),
        ('solved', 'Solved'),
    ]

    ticket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    image_upload = models.ImageField(upload_to='ticket_images/', blank=True, null=True)
    submit_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        db_table = 'support_ticket'

# Custom function to set the initial value
@receiver(pre_save, sender=support_ticket)
def set_initial_ticket_id(sender, instance, **kwargs):
    if not instance.pk:
        # Only set the ticket_id if it's a new record
        max_id = support_ticket.objects.aggregate(max_id=models.Max('ticket_id'))['max_id']
        if max_id is None:
            instance.ticket_id = 1000000
        else:
            instance.ticket_id = max_id + 1


class ticket_discussion(models.Model):
    ticket = models.ForeignKey(support_ticket, on_delete=models.CASCADE)
    sender = models.ForeignKey(user_registration, on_delete=models.CASCADE, null=True)
    is_user = models.BooleanField()  
    message = models.TextField()
    file_upload = models.FileField(upload_to='discussion_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket_discussion'




class notification_centre(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification_centre'



class earning_centre(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    total_earned = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    withdrawn_amount = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    

    class Meta:
        db_table = 'earning_centre'




class image_rating_review(models.Model):
    star_rating = models.IntegerField()
    image_review = models.TextField()
    purchased_id = models.ForeignKey(purchased_items, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'image_review'




class user_verification(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    full_name = models.TextField()
    phone = models.IntegerField()
    age = models.IntegerField()
    profession = models.TextField()
    identity_file = models.FileField(upload_to='identity_files/')
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.TextField(default="pending")

    class Meta:
        db_table = 'user_verification'


class withdrawal_request(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('bank', 'Bank')])
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    comission = models.DecimalField(max_digits=10, decimal_places=2)
    to_be_paid = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'withdrawal_request'

