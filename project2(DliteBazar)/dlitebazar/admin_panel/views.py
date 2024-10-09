import datetime
from django.shortcuts import render, redirect, get_object_or_404
from user_registration.models import user_registration
from profile_dashboard.models import upload_images, liked_images, purchased_items, support_ticket, ticket_discussion, notification_centre, earning_centre, image_rating_review, user_verification, withdrawal_request, contact_us

from django.utils.timezone import now, timedelta
from django.db.models import Sum
from django.db import models
from django.db.models import Q
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from collections import defaultdict

from django.utils import timezone


def dashboard(request):

    total_users = user_registration.objects.count()
    total_images = upload_images.objects.count()
    active_users = user_registration.objects.filter(is_active=True).count()
    verified_users = user_registration.objects.filter(is_verified=True).count()

    today = now().date()
    todays_registrations = user_registration.objects.filter(date_joined__date=today).count()
    todays_uploads = upload_images.objects.filter(uploaded_datetime__date=today).count()
    pending_complaints = support_ticket.objects.filter(status='pending').count()
    withdrawal_requests = withdrawal_request.objects.filter(status='pending').count()

    total_liked_images = liked_images.objects.count()
    total_purchases = purchased_items.objects.count()
    total_earnings = int(earning_centre.objects.aggregate(total=models.Sum('total_earned'))['total'] or 0)
    total_notifications = notification_centre.objects.count()
    total_comission = withdrawal_request.objects.aggregate(total=Sum('comission'))['total']
    total_discount = purchased_items.objects.aggregate(total=Sum('discounted_amount'))['total']
    total_profit = total_comission-total_discount

    context = {
        'total_users': total_users,
        'total_images': total_images,
        'active_users': active_users,
        'verified_users': verified_users,
        'todays_registrations': todays_registrations,
        'todays_uploads': todays_uploads,
        'pending_complaints': pending_complaints,
        'withdrawal_requests': withdrawal_requests,
        'total_liked_images': total_liked_images,
        'total_purchases': total_purchases,
        'total_earnings': total_earnings,
        'total_notifications': total_notifications,
        'total_comission': total_comission,
        'total_discount': total_discount,
        'total_profit': total_profit
    }

    return render(request, 'dashboard.html', {'context':context})



def user_management(request):

    users = user_registration.objects.all()
    context = {
        'users': users,
    }

    if request.method == 'POST' and 'search' in request.POST:
        search_query = request.POST.get('search_query', '').strip()
        if search_query:
            users = users.filter(
                Q(username__icontains=search_query) |
                Q(user_id__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(middle_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
            context = {
                'users': users,
                 }

    return render(request, 'users.html', {'context':context})

def edit_user(request, user_id):


    user = get_object_or_404(user_registration, user_id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.middle_name = request.POST.get('middle_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number = request.POST.get('phone_number')
        user.address = request.POST.get('address')
        user.postal_code = request.POST.get('postal_code')
        user.is_verified = request.POST.get('is_verified') == 'on'
        user.is_email_notification = request.POST.get('is_email_notification') == 'on'
        user.save()
        notification_centre.objects.create(
                            user = user,
                            event_type = 'edit info',
                            message = "Your profile information is edited by admin!!",
                        )
        if user.is_email_notification:
            email = user.email
            send_mail(
                    'Edited Profile Information',
                    f'Your profile information is edited by admin!! please check profile dashboard. ',
                    'project020g@gmail.com',
                    [email],
                    fail_silently=False
                )

        return redirect('user_management')
    
    context = {
        'user': user,
    }
    return render(request, 'edit_user.html', context)

def deactivate_user(request, user_id):

    user = get_object_or_404(user_registration, user_id=user_id)
    user.is_active = False
    user.save()
    notification_centre.objects.create(
                            user = user,
                            event_type = 'deactive',
                            message = "Your account was deactivated by admin!!",
                        )
    
    email = user.email
    send_mail(
                    'Account deactivated',
                    f'Your Account got deactivated for fraud activity!!',
                    'project020g@gmail.com',
                    [email],
                    fail_silently=False
                )
    return redirect('user_management')

def activate_user(request, user_id):


    user = get_object_or_404(user_registration, user_id=user_id)
    user.is_active = True
    user.save()
    
    notification_centre.objects.create(
                            user = user,
                            event_type = 'active',
                            message = "Your account is activated by admin!!",
                        )
    
    email = user.email
    send_mail(
                    'Account Activated successfully',
                    f'Your Account is activated again!!',
                    'project020g@gmail.com',
                    [email],
                    fail_silently=False
                )

    return redirect('user_management')



def image_management(request):


    images = upload_images.objects.all()

    if request.method == "POST" and 'image_search' in request.POST:
        search_query = request.POST.get('search_query', '').strip()
        if search_query:
            images = images.filter(
                Q(title__icontains=search_query) |
                Q(category__icontains=search_query) |
                Q(subcategory__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(keywords__icontains=search_query) |
                Q(image_id__icontains=search_query)
            )
            

    return render(request, 'images.html', {'images': images})


def deactivate_image(request, image_id):

    image = upload_images.objects.get(image_id=image_id)
    image.is_active = False
    image.save()

    notification_centre.objects.create(
                            user = image.user,
                            event_type = 'image delete',
                            message = f"Your image title:{image.title} is deleted from server!!",
                        )
    
    email = image.user.email
    send_mail(
                    'Image deleted',
                    f'Your image title:{image.title} is deleted from server!!',
                    'project020g@gmail.com',
                    [email],
                    fail_silently=False
                )

    return redirect('image_management')

def activate_image(request, image_id):

    image = upload_images.objects.get(image_id=image_id)
    image.is_active = True
    image.save()
    return redirect('image_management')




def withdrawal_requests(request):


    pending_requests = withdrawal_request.objects.filter(status='pending').order_by('request_date')
    approved_requests = withdrawal_request.objects.filter(status='approved').order_by('-request_date')
    rejected_requests = withdrawal_request.objects.filter(status='rejected').order_by('-request_date')

    context = {
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
    }
    return render(request, 'withdrawals.html', {'context':context})

def approve_withdrawal(request, request_id):

    withdrawal = get_object_or_404(withdrawal_request, id=request_id)
    withdrawal.status = 'approved'
    withdrawal.save()

    notification_centre.objects.create(
                            user = withdrawal.user,
                            event_type = 'approval withdrawn',
                            message = f"Your request for Rs:{withdrawal.amount} is Approved, check your bank account!!",
                        )
    
    email = withdrawal.user.email
    send_mail(
                    'Withdrawal approved',
                    f"Your request for Rs:{withdrawal.amount} is Approved, check your bank account!!",
                    'project020g@gmail.com',
                    [email],
                    fail_silently=False
                )

    return redirect('withdrawal_requests')

def reject_withdrawal(request, request_id):

    withdrawal = get_object_or_404(withdrawal_request, id=request_id)
    withdrawal.status = 'rejected'
    user = withdrawal.user
    change_earning = get_object_or_404(earning_centre, user=user)
    change_earning.withdrawn_amount -= withdrawal.amount
    change_earning.save()
    withdrawal.save()

    notification_centre.objects.create(
                            user = withdrawal.user,
                            event_type = 'Withdrawal Rejected',
                            message = f"Your request for Rs:{withdrawal.amount} is Rejected, Try again requesting!!",
                        )
    
    email = withdrawal.user.email
    send_mail(
                    'Withdrawal Rejected',
                    f"Your request for Rs:{withdrawal.amount} is Rejected, Try again requesting!!",
                    'project020g@gmail.com',
                    [email],
                    fail_silently=False
                )

    return redirect('withdrawal_requests')




def complaints_section(request):

    search_query = request.GET.get('search_query', '')

    if search_query:
        pending_tickets = support_ticket.objects.filter(
            Q(status='pending') & (
                Q(ticket_id__icontains=search_query) |
                Q(user__user_id__icontains=search_query) |
                Q(subject__icontains=search_query)
            )
        ).order_by('submit_datetime')

        progress_tickets = support_ticket.objects.filter(
            Q(status='progress') & (
                Q(ticket_id__icontains=search_query) |
                Q(user__user_id__icontains=search_query) |
                Q(subject__icontains=search_query)
            )
        ).order_by('submit_datetime')

        solved_tickets = support_ticket.objects.filter(
            Q(status='solved') & (
                Q(ticket_id__icontains=search_query) |
                Q(user__user_id__icontains=search_query) |
                Q(subject__icontains=search_query)
            )
        ).order_by('submit_datetime')
    else:
        pending_tickets = support_ticket.objects.filter(status='pending').order_by('submit_datetime')
        progress_tickets = support_ticket.objects.filter(status='progress').order_by('submit_datetime')
        solved_tickets = support_ticket.objects.filter(status='solved').order_by('submit_datetime')

    context = {
        'pending_tickets': pending_tickets,
        'progress_tickets': progress_tickets,
        'solved_tickets': solved_tickets,
        'search_query': search_query,
    }


    return render(request, 'complaints.html', {'context':context})


def ticket_details(request, ticket_id):


    ticket = get_object_or_404(support_ticket, ticket_id=ticket_id)
    discussions = ticket_discussion.objects.filter(ticket=ticket).order_by('-timestamp')

    if request.method == 'POST' and 'submit_discussion' in request.POST:
        message = request.POST.get('message')
        file_upload = request.FILES.get('file_upload')
        if file_upload:
            fs = FileSystemStorage(location='media/discussion_files/')
            filename = fs.save(file_upload.name, file_upload)
            uploaded_document = 'discussion_files/' + filename
        else:
            uploaded_document=None
        if message:
            ticket_discussion.objects.create(
                ticket=ticket,
                sender=None,  
                is_user=False,  
                message=message,
                file_upload=uploaded_document,
                timestamp=timezone.now()
            )
            ticket.status = 'progress'
            ticket.save()
            notification_centre.objects.create(
                            user = ticket.user,
                            event_type = 'ticket progress',
                            message = f"Admin messaged for your ticket title:{ticket.subject}",
                        )

            return redirect('ticket_details', ticket_id=ticket_id)

    context = {
        'ticket': ticket,
        'discussions': discussions,
    }
    return render(request, 'ticket_details.html', {'context':context})




def user_verification_requests(request):
    
    verification_sections = {
        'pending': defaultdict(list),
        'accepted': defaultdict(list),
        'rejected': defaultdict(list),
    }

    if request.method == 'POST' and 'search' in request.POST:
        search_query = request.POST['search_query']
        user_filter = Q(user__email__icontains=search_query) | Q(user__first_name__icontains=search_query) | \
                      Q(user__last_name__icontains=search_query) | Q(user__username__icontains=search_query) | \
                      Q(user__user_id__icontains=search_query)
        verification_requests = user_verification.objects.filter(user_filter)
    else:
        verification_requests = user_verification.objects.all()

    for verification_request in verification_requests:
        verification_sections[verification_request.status][verification_request.requested_at.date()].append(verification_request)

    verification_sections = {status: dict(days) for status, days in verification_sections.items()}

    return render(request, 'user_verification_request.html', {'verification_sections': verification_sections})


def accepted_document(request, verification_id):
    user_document = user_verification.objects.get(id=verification_id)
    user_document.status = 'accepted'
    user_document.save()
    user = user_document.user
    user.is_verified=True
    user.save()
    notification_centre.objects.create(
                            user = user,
                            event_type = 'account verification',
                            message = "Your request for account verification is successful!! you can upload and sell images now. Thanks for your valuable time.",
                        )
    email = user.email
    send_mail(
                    'Account Verification',
                    "Your request for account verification is successful!! you can upload and sell images now. Thanks for your valuable time.",
                    'project020g@gmail.com',
                    [email],
                    fail_silently=False
                )

    return redirect('user_verification_requests')


def rejected_document(request, verification_id):
    user_document = user_verification.objects.get(id=verification_id)
    user_document.status = 'rejected'
    user_document.save()
    user = user_document.user
    user.is_verified=False
    user.save()
    notification_centre.objects.create(
                            user = user,
                            event_type = 'account verification',
                            message = "Your request for account verification is Rejected!! please submit clear and original id document of yours!! thanks",
                        )
    email = user.email
    send_mail(
                    'Account Verification',
                    "Your request for account verification is Rejected!! please submit clear and original id document of yours!! thanks",
                    'project020g@gmail.com',
                    [email],
                    fail_silently=False
                )

    return redirect('user_verification_requests')


def contact_us_data(request):
    pending_contacts = contact_us.objects.filter(status='pending').order_by('id')

    emailed_contacts = contact_us.objects.filter(status='emailed')


    return render(request, 'contact_us.html', {'pending_contacts':pending_contacts, 'emailed_contacts':emailed_contacts})


def admin_login(request):
    error=None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        if username == 'admin' and password=='admin123':
            return redirect('dashboard')
        else:
            error = 'invalid username or password!!'
    return render(request, 'admin_login.html', {'error':error})




def send_email(request, contact_id):
    contact = contact_us.objects.get(id=contact_id)
    if request.method == 'POST' and 'contact_email' in request.POST:
        email_body = request.POST.get('email_body')
        if email_body:
            email = contact.email
            send_mail(
                'DliteBazar | Response to your Message',
                email_body,
                'from@example.com',
                [email],
                fail_silently=False,
            )
            
            contact.status='emailed'
            contact.save()
            return redirect('contact_us')
    return render(request, 'send_email.html',{'email':contact.email})
