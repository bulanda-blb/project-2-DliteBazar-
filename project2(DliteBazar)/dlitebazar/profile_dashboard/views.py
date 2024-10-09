from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from user_registration.models import user_registration
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from PIL import Image
from .models import upload_images, liked_images, purchased_items, support_ticket, ticket_discussion, notification_centre, earning_centre, image_rating_review, user_verification, withdrawal_request

from decimal import Decimal
from collections import defaultdict
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.core.mail import send_mail

def profile_page(request):
    if not request.session.get('active_user') and not request.session.get('user_id'):
        request.session.flush()
        return redirect('home_page')
    else:
        user_id = request.session.get('user_id')
        user = user_registration.objects.get(user_id=user_id)

        try:
            notifications = notification_centre.objects.filter(user=user).order_by('-created_at')
        except notification_centre.DoesNotExist:
            notifications=None    
        top1_notification = None
        top2_notification = None
        top3_notification = None
        top4_notification = None
        
        # Assign notifications based on their count
        if notifications.count() > 0:
            top1_notification = notifications[0]
        if notifications.count() > 1:
            top2_notification = notifications[1]
        if notifications.count() > 2:
            top3_notification = notifications[2]
        if notifications.count() > 3:
            top4_notification = notifications[3]

        context = {
            'notification1': top1_notification,
            'notification2': top2_notification,
            'notification3': top3_notification,
            'notification4': top4_notification,

        }

        profile_picture = user.profile_picture
        if profile_picture:
            profile_picture = profile_picture
        else:
            profile_picture = None    
        try:
            images = upload_images.objects.filter(user=user, is_active=True)
        except upload_images.DoesNotExist:
            images=None
        try:    
            purchased_images = purchased_items.objects.filter(purchased_by=user)
        except purchased_items.DoesNotExist:
            purchased_images=None    
        try:
            sold_images = purchased_items.objects.filter(purchase_from=user)
        except purchased_items.DoesNotExist:
            sold_images = None
        try:
            earning = earning_centre.objects.get(user=user)
        except earning_centre.DoesNotExist:
            earning = None

        if earning:
            total_earning = earning.total_earned
            remaining_withdrwan = total_earning - earning.withdrawn_amount
        else:
            total_earning = None
            remaining_withdrwan = None

        support_tickets = support_ticket.objects.filter(user=user)

        ticket_discussed = ticket_discussion.objects.filter(
        Q(sender=user) | Q(sender_id=None)
        ).order_by('-timestamp')

        full_name = f"{user.first_name} {user.middle_name if user.middle_name else ''} {user.last_name}".strip()

        try:
            verification_requests = user_verification.objects.get(user=user, status='pending')
        except user_verification.DoesNotExist:
            verification_requests=None


        if request.method == "POST":
            if "logout" in request.POST:
                notification_centre.objects.create(
                            user = user,
                            event_type = 'logout',
                            message = "Last logout: ",
                        )
                request.session.flush()
                return redirect('home_page')

            if request.FILES.get('profile_picture'):
                profile_picture = request.FILES.get('profile_picture')
                fs = FileSystemStorage(location='media/profile_pictures/')
                filename = fs.save(profile_picture.name, profile_picture)
                user.profile_picture = 'profile_pictures/' + filename
                user.save()
                notification_centre.objects.create(
                            user = user,
                            event_type = 'profile_pic_change',
                            message = "Your profile picture changed successfully!! ",
                        )
                return redirect('profile_page')

            if 'section' in request.POST:
                section = request.POST.get('section')
                if section == 'phone':
                    phone_number = request.POST.get('phone-number')
                    user.phone_number = phone_number
                    notification_centre.objects.create(
                            user = user,
                            event_type = 'number_change',
                            message = f"Your phone number changed successfully!! to {phone_number} ",
                        )
                elif section == 'address':
                    address_line = request.POST.get('address-line1')
                    postal_code = request.POST.get('postal-code')
                    user.address = address_line
                    user.postal_code = postal_code
                    notification_centre.objects.create(
                            user = user,
                            event_type = 'address_postal_change',
                            message = f"Your address and postal code changed successfully!! to {address_line},{postal_code} ",
                        )
                user.save()
                return redirect('profile_page')

            
            if 'upload_images' in request.POST:
                image_file = request.FILES.get('imageFile')
                fs = FileSystemStorage(location='media/uploaded_images/')
                filename = fs.save(image_file.name, image_file)
                uploaded_image = 'uploaded_images/' + filename

                title = request.POST.get('title')
                category = request.POST.get('category')
                subcategory = request.POST.get('subcategory')
                description = request.POST.get('description')
                price = request.POST.get('price')
                keywords = request.POST.get('keywords')

                size = image_file.size / 1024
                with Image.open(image_file) as img:
                    
                    dpi = img.info.get('dpi', (72, 72))[0]
                    file_format = img.format
                    resolution = f"{img.width}x{img.height}"

                upload_images.objects.create(
                    user=user,
                    image_file=uploaded_image,
                    title=title,
                    category=category,
                    subcategory=subcategory,
                    description=description,
                    price=price,
                    keywords=keywords,
                    size=int(size),
                    resolution=resolution,
                    file_format=file_format,
                    dpi=dpi,
                    uploaded_datetime=timezone.now(),
                    sold_multiple_counter=0,
                    liked_by_counter=0
                )
                notification_centre.objects.create(
                            user = user,
                            event_type = 'upload_image',
                            message = f"Your image have been uploaded successfully!! with title {title} ",
                        )
                return redirect('profile_page')
            
            if 'ticket_submit' in request.POST:
                subject = request.POST.get('ticketSubject')
                description = request.POST.get('ticketDescription')
                image_upload = request.FILES.get('ticketAttachment')
                if image_upload:
                    fs = FileSystemStorage(location='media/ticket_images/')
                    filename = fs.save(image_upload.name, image_upload)
                    uploaded_image = 'ticket_images/' + filename

                    support_ticket.objects.create(
                        user=user,
                        subject=subject,
                        description=description,
                        image_upload=uploaded_image,
                        submit_datetime=timezone.now()
                    )
                    notification_centre.objects.create(
                            user = user,
                            event_type = 'ticket_entry',
                            message = f"We received your ticket, wait for response!! subject: {subject} ",
                        )
                    if user.is_email_notification:
                        email=user.email
                        send_mail(
                                'Ticket Entry',
                                f"We received your ticket, wait for response!! subject: {subject} ",
                                'project020g@gmail.com',
                                [email],
                                fail_silently=False
                            )
                else:
                    support_ticket.objects.create(
                        user=user,
                        subject=subject,
                        description=description,
                        image_upload=None,
                        submit_datetime=timezone.now()
                    )
                    notification_centre.objects.create(
                            user = user,
                            event_type = 'ticket_entry',
                            message = f"We received your ticket, wait for response!! subject: {subject} ",
                        )
                    if user.is_email_notification:
                        email=user.email
                        send_mail(
                                'Ticket Entry',
                                f"We received your ticket, wait for response!! subject: {subject} ",
                                'project020g@gmail.com',
                                [email],
                                fail_silently=False
                            )


            if 'submit_discussion' in request.POST:
                ticket_id = request.POST.get('ticket_id')
                ticket = support_ticket.objects.get(ticket_id=ticket_id)
                message = request.POST.get('discuss_message')
                image_upload = request.FILES.get('discussion_file')
                if image_upload:
                    
                    fs = FileSystemStorage(location='media/discussion_files/')
                    filename = fs.save(image_upload.name, image_upload)
                    uploaded_image = 'discussion_files/' + filename
                    ticket_discussion.objects.create(
                        ticket=ticket,
                        sender=user,
                        is_user = True,
                        message = message,
                        file_upload = uploaded_image
                    )
                else:
                    ticket_discussion.objects.create(
                        ticket=ticket,
                        sender=user,
                        is_user = True,
                        message = message,
                        file_upload = None
                    )


        return render(request, 'profile.html', {'user':user, 'support_tickets':support_tickets, 'ticket_discussed':ticket_discussed, 'sold_images':sold_images,'purchased_images':purchased_images, 'profile_picture':profile_picture, 'full_name':full_name, 'images':images, 'notifications':notifications, 'context':context, 'total_earning':total_earning, 'remaining_withdrawn':remaining_withdrwan, 'verification_requests':verification_requests})



def edit_image_details(request, image_id):
    if not request.session.get('active_user') and not request.session.get('user_id'):
        request.session.flush()
        return redirect('user_login')
    else:
        user_id = request.session.get('user_id')
        user = user_registration.objects.get(user_id=user_id)
        try:
            image = upload_images.objects.get(image_id=image_id, user=user, is_active=True)
        except upload_images.DoesNotExist:
            image=None
            return redirect('profile_page')
        
        if request.method == 'POST':
            if 'edit_image' in request.POST:
                title = request.POST.get('title')
                description = request.POST.get('description')
                keywords = request.POST.get('keywords')
                price = request.POST.get('price')
                category = request.POST.get('category')
                subcategory = request.POST.get('subcategory')

                image.title = title
                image.description = description
                image.keywords = keywords
                image.price = price
                image.category = category
                image.subcategory = subcategory
                image.save()
                notification_centre.objects.create(
                                user = user,
                                event_type = 'image_edit',
                                message = f"image information is edited successfully!! title: {title} ",
                            )
                # return render(request, 'edit_image_details.html', {'image':image})
                return redirect(reverse('edit_image', args=[image_id]))
            if 'delete_image' in request.POST:
                value = request.POST.get('delete_ok')
                if not image.sold_multiple_counter and not image.liked_by_counter:
                    if value == "ok":
                        image.is_active = False
                        image.save()
                        notification_centre.objects.create(
                                user = user,
                                event_type = 'image_delete',
                                message = f"image information is deleted successfully!! title: {image.title} ",
                            )
                        if user.is_email_notification:
                            email=user.email
                            send_mail(
                                'image deleted',
                                f"image information is deleted successfully!! title: {image.title} ",
                                'project020g@gmail.com',
                                [email],
                                fail_silently=False
                            )
                        return redirect('profile_page')

    return render(request, 'edit_image_details.html', {'image':image})



def checkout(request, image_id):
    is_active = request.session.get('active_user')
    user_id = request.session.get('user_id')
    if is_active and user_id:
        user = user_registration.objects.get(user_id=user_id)   

    else:
        user = None

    if not request.session.get('active_user') and not request.session.get('user_id'):
        
        request.session['try_to_checkout'] = image_id
        request.session.set_expiry(3600)
        return redirect('user_login')
    else:
        user_id = request.session.get('user_id')
        user = user_registration.objects.get(user_id=user_id)
        try:
            image = upload_images.objects.get(image_id=image_id)
        except upload_images.DoesNotExist:
            image=None
            return redirect('profile_page')
        earn_rewards = int(image.price)
        if user.reward_points:
            rewards = int(user.reward_points)
            available_reward_point = user.reward_points
            discounted_coupon = available_reward_point/Decimal(1000.00)
            if discounted_coupon>=image.price:
                discounted_coupon = image.price - Decimal(100.00)
                total_amount = 100.00
            else:
                total_amount = image.price - discounted_coupon
        else:
            rewards = 0
            discounted_coupon = 0.00
            total_amount = image.price
        try:    
            alreay_purchased = purchased_items.objects.get(purchased_by=user, image=image)
        except purchased_items.DoesNotExist:
            alreay_purchased = None
        if alreay_purchased:
            profile_url = reverse('profile_page')
            html_content = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Redirect to Profile</title>
                    
                </head>
                <body>
                    <h1>Image already purchased</h1>
                    <p>Click the button below to go to your profile:</p>
                    <a href="{profile_url}" class="button">Go to Profile</a>
                </body>
                </html>
                """

            return HttpResponse(html_content) 
    if request.method == 'POST' and 'purchase' in request.POST:
        email = user.email
        address= request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method= request.POST.get('payment_method')
        image= image
        purchased_by= user
        purchase_from= image.user
        purchase_date=timezone.now()
        
        if user.reward_points:
            available_reward_point = user.reward_points
            discounted_coupon = available_reward_point/Decimal(1000.00)
            if discounted_coupon>=image.price:
                discounted_coupon = image.price - Decimal(100.00)
                paid_amount = image.price - discounted_coupon
                remaining_reward_point = available_reward_point - discounted_coupon*Decimal(1000.00)
            else:
                paid_amount = image.price - discounted_coupon
                remaining_reward_point = Decimal(0.00)
        else:
            discounted_coupon = Decimal(0.00)
            paid_amount = image.price
            remaining_reward_point = Decimal(0.00)
        try:
            earning = earning_centre.objects.get(user=purchase_from)
        except earning_centre.DoesNotExist:
            earning = None    

        purchased_items.objects.create(
            email = email,
            address = address,
            phone = phone,
            payment_method = payment_method,
            image = image,
            purchased_by = purchased_by,
            purchase_from = purchase_from,
            purchase_date = purchase_date,
            payment_success = True,
            discounted_amount = discounted_coupon,
            paid_amount = paid_amount
        )

        if earning:
            total_earned = earning.total_earned
            new_total_earned = image.price + total_earned
            earning.total_earned = new_total_earned
            earning.save()
        else:
            total_earned = image.price
            withdrawn_amount = Decimal('0.00')
            earning_centre.objects.create(
                total_earned = total_earned,
                user = purchase_from,
                withdrawn_amount = withdrawn_amount
            )

        user.reward_points = remaining_reward_point + image.price
        user.save()

        image.sold_multiple_counter += 1
        image.save()
        notification_centre.objects.create(
                            user = user,
                            event_type = 'image_purchase',
                            message = f"Successfully purchased!! image: {image.title} ",
                        )
        buyer_email=user.email
        send_mail(
                        'image_purchase',
                        f"Successfully purchased!! image: {image.title} ",
                        'project020g@gmail.com',
                        [buyer_email],
                        fail_silently=False
                   )
                    
        notification_centre.objects.create(
                            user = image.user,
                            event_type = 'image_sold',
                            message = f"Congratulations your image got sold!! image: {image.title} ",
                        )
        owner_email = image.user.email
        send_mail(
                        'image sold',
                        f"Congratulations your image got sold!! image: {image.title} ",
                        'project020g@gmail.com',
                        [owner_email],
                        fail_silently=False
                   )
        return redirect('profile_page')

    return render(request, 'checkout.html', {'image':image, 'is_active':is_active, 'user':user, 'discount':discounted_coupon, 'total':total_amount, 'rewards':rewards, 'earn':earn_rewards})






def purchased_image_details(request, purchased_id):
    if not request.session.get('active_user') and not request.session.get('user_id'):
        request.session.flush()
        return redirect('user_login')
    else:
        is_active = request.session.get('active_user')
        user_id = request.session.get('user_id')
        if is_active and user_id:
            user = user_registration.objects.get(user_id=user_id)   

        else:
            user = None
        try:    
            purchased_details = purchased_items.objects.get(id=purchased_id, purchased_by=user)
        except purchased_items.DoesNotExist:
            purchased_details=None
            return redirect('profile_page')    
        try:
            rating_data = image_rating_review.objects.get(purchased_id=purchased_id)
        except image_rating_review.DoesNotExist:
            rating_data = None

        if request.method=='POST':
            if 'review' in request.POST:
                rating = request.POST.get('rating')
                review = request.POST.get('feedback')

                image_rating_review.objects.create(
                    star_rating = rating,
                    image_review = review,
                    purchased_id = purchased_details
                )
                notification_centre.objects.create(
                                user = user,
                                event_type = 'rating',
                                message = f"we received your review!! image:{purchased_details.image.title} ",
                            )
                notification_centre.objects.create(
                                user = purchased_details.purchase_from,
                                event_type = 'rating',
                                message = f"congratulations your image got reviewed!!: image: {purchased_details.image.title} ",
                            )
                return redirect(reverse('purchased_image_details', args=[purchased_id]))
                
            if 'edit_review' in request.POST:
                edit_rating = request.POST.get('edit_rating')
                edit_review = request.POST.get('edit_feedback')
                rating_data.star_rating=edit_rating
                rating_data.image_review=edit_review
                rating_data.save()

                notification_centre.objects.create(
                                user = user,
                                event_type = 'rating',
                                message = f"review edited successfully!! image:{purchased_details.image.title} ",
                            )
                notification_centre.objects.create(
                                user = purchased_details.purchase_from,
                                event_type = 'rating',
                                message = f"your image reviewe is edited!!: image: {purchased_details.image.title} ",
                            )
                return redirect(reverse('purchased_image_details', args=[purchased_id]))

        return render(request, 'purchased_image_details.html', {'purchased_details':purchased_details, 'rating_data':rating_data})


def sold_image_details(request, sold_id):
    if not request.session.get('active_user') and not request.session.get('user_id'):
        request.session.flush()
        return redirect('user_login')
    else:
        is_active = request.session.get('active_user')
        user_id = request.session.get('user_id')
        if is_active and user_id:
            user = user_registration.objects.get(user_id=user_id)   

        else:
            user = None
        try:
            sold_details = purchased_items.objects.get(id=sold_id, purchase_from=user)
        except purchased_items.DoesNotExist:
            sold_details=None
            return redirect('profile_page')    
        try:
            rating_data = image_rating_review.objects.get(purchased_id=sold_id)
        except image_rating_review.DoesNotExist:
            rating_data = None

    return render(request, 'sold_image_details.html', {'sold_details':sold_details,'rating_data':rating_data})




def user_verification_centre(request):
    if not request.session.get('active_user') and not request.session.get('user_id'):
        request.session.flush()
        return redirect('user_login')
    else:
        is_active = request.session.get('active_user')
        user_id = request.session.get('user_id')
        if is_active and user_id:
            user = user_registration.objects.get(user_id=user_id)   

        else:
            user = None
    valid_error={}
    if request.method == 'POST' and 'verify' in request.POST:
        full_name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        age = request.POST.get('age')
        profession = request.POST.get('profession')
        identity_document = request.FILES.get('identity_document')

        if not full_name:
            valid_error['fullname'] = "Enter full name!!"
        if not phone_number:
            valid_error['phone'] = "Enter phone number!!"
        if not age:
            valid_error['age'] = "Enter your age!!"
        if not profession:
            valid_error['profession'] = "Enter Your profession!!"
        if not identity_document:
            valid_error['document'] = "Upload Your real document!!"
        
        if identity_document:
            fs = FileSystemStorage(location='media/identity_files/')
            filename = fs.save(identity_document.name, identity_document)
            uploaded_document = 'identity_files/' + filename

        if not valid_error and user:
            user_verification.objects.create(
                user = user,
                full_name=full_name,
                phone=phone_number,
                age=age,
                profession=profession,
                identity_file = uploaded_document

            )
            notification_centre.objects.create(
                                user = user,
                                event_type = 'verification',
                                message = "We received your verification request, please wait for response!! ",
                            )
            if user.is_email_notification:
                    email=user.email
                    send_mail(
                        'Verification request',
                        f"We received your verification request, please wait for response!!",
                        'project020g@gmail.com',
                        [email],
                        fail_silently=False
                    )
            return redirect('profile_page')

    return render(request, 'user_verification.html', {'valid_error':valid_error})




def notifications(request):
    if not request.session.get('active_user') and not request.session.get('user_id'):
        request.session.flush()
        return redirect('user_login')
    else:
        is_active = request.session.get('active_user')
        user_id = request.session.get('user_id')
        if is_active and user_id:
            user = user_registration.objects.get(user_id=user_id)   

        else:
            user = None
    notifications = notification_centre.objects.filter(user=user).order_by('-created_at')

    grouped_notifications = {}
    for notification in notifications:
        date_str = DateFormat(notification.created_at).format('Y-m-d')
        if date_str not in grouped_notifications:
            grouped_notifications[date_str] = []
        grouped_notifications[date_str].append(notification)


    return render(request, 'notifications.html', {'user': user, 'grouped_notifications': grouped_notifications})



@require_POST
def toggle_email_notification(request):
    if not request.session.get('active_user') and not request.session.get('user_id'):
        request.session.flush()
        return redirect('user_login')
    
    user_id = request.session.get('user_id')
    user = user_registration.objects.get(user_id=user_id)

    # Toggle the email notification flag
    user.is_email_notification = not user.is_email_notification
    user.save()

    return redirect('notifications')




def transactions(request):
    if not request.session.get('active_user') and not request.session.get('user_id'):
        request.session.flush()
        return redirect('user_login')
    else:
        valid_error={}
        is_active = request.session.get('active_user')
        user_id = request.session.get('user_id')
        if is_active and user_id:
            user = user_registration.objects.get(user_id=user_id)   
        else:
            user = None
            

    if user:
        try:
            earnings = earning_centre.objects.get(user=user)
        except earning_centre.DoesNotExist:
            earnings=None    
        sold_images = purchased_items.objects.filter(purchase_from=user, payment_success=True).order_by('-purchase_date')
        if earnings:
            total_earned = earnings.total_earned or 0
            withdrawn_amount = earnings.withdrawn_amount or 0
            remaining_balance = total_earned - withdrawn_amount
        else:
            total_earned = 0
            withdrawn_amount = 0
            remaining_balance = 0

        if not remaining_balance:
            valid_error['remaining_balance'] = "You don't have balance to withdraw amount!!"
        # Group earnings by month
        grouped_earnings = defaultdict(list)
        for item in sold_images:
            month_str = item.purchase_date.strftime('%Y-%m')
            grouped_earnings[month_str].append(item)

        withdrawals = withdrawal_request.objects.filter(user=user).order_by('status', '-request_date')
    
        grouped_withdrawals = defaultdict(list)
        for withdrawal in withdrawals:
            month_str = DateFormat(withdrawal.request_date).format('Y-m')
            grouped_withdrawals[month_str].append(withdrawal)

        context = {
        'total_earned': total_earned,
        'withdrawn_amount': withdrawn_amount,
        'remaining_balance': remaining_balance,
        'grouped_earnings': dict(grouped_earnings),
        'grouped_withdrawals': dict(grouped_withdrawals),
        }

        if request.method == 'POST' and 'withdraw_request' in request.POST:
            amount = request.POST.get('amount')
            payment_method = request.POST.get('payment_method')
            account_name = request.POST.get('account_name')
            account_number = request.POST.get('account_number')
            bank_name = request.POST.get('bank_name')

            if not amount:
                valid_error['amount'] = "Enter amount for withdrawl!!"
            if not payment_method:
                valid_error['payment_method'] = "Enter Payment method to withdraw amount!!"
            if not account_name:
                valid_error['account_name'] = "Account name is required!!"
            if not account_number:
                valid_error['account_number'] = "Account number is required!!"
            if not bank_name:
                valid_error['bank_name'] = "Bank name is required!!"
            if Decimal(amount)>remaining_balance:
                valid_error['amount_exceed'] = "You can't enter amount more than remaining!!"

            if not valid_error:
                comission = int(amount) * 0.1
                comission = Decimal(comission)
                transfer_amount = Decimal(amount)
                to_be_paid = Decimal(amount)-comission
                withdrawal_request.objects.create(
                    user=user,
                    amount=transfer_amount,
                    payment_method=payment_method,
                    account_name=account_name,
                    account_number=account_number,
                    bank_name=bank_name,
                    comission = comission,
                    to_be_paid = to_be_paid

                )
                earnings.withdrawn_amount = withdrawn_amount + Decimal(amount)
                earnings.save()
                notification_centre.objects.create(
                                user = user,
                                event_type = 'withdraw',
                                message = f"We received your withdrawal request, amount:{amount} please wait!! ",
                            )
                if user.is_email_notification:
                    email=user.email
                    send_mail(
                        'Withdraw request',
                        f"We received your withdrawal request, amount:{amount} please wait!! ",
                        'project020g@gmail.com',
                        [email],
                        fail_silently=False
                    )
                return redirect('transactions')
    return render(request, 'transactions.html',{'context':context, 'valid_error':valid_error})



def complaint_solved(request, ticket_id):
    ticket = support_ticket.objects.get(ticket_id=ticket_id)
    ticket.status = 'solved'
    ticket.save()
    notification_centre.objects.create(
                                user = ticket.user,
                                event_type = 'complaint solved',
                                message = f"Your complaint ticket title:{ticket.subject} is solved according to you!!",
                            )
    if ticket.user.is_email_notification:
        email = ticket.user.email
        send_mail(
                        'Complaint ticket solved',
                        f"Your complaint ticet title:{ticket.subject} is solved according to your discussion. please feel free to contact if any issues arises!!",
                        'project020g@gmail.com',
                        [email],
                        fail_silently=False
                    )
    return redirect('profile_page')



