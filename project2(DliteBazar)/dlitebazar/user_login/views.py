
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from user_registration.models import user_registration
from profile_dashboard.models import notification_centre, upload_images
from django.contrib.auth.hashers import check_password, make_password

import random
import time
import re
from django.core.mail import send_mail


def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)


def user_login(request):
    try_to_checkout = request.session.get('try_to_checkout')
    if request.session.get('active_user') and request.session.get('user_id'):

        return redirect('profile_page')
    else:
        empty_error = {}
        valid_error = {}
        user = None
        
        if request.method == 'POST':
                email = request.POST.get('email')
                password = request.POST.get('password')
                
                if not email:
                    empty_error['empty_email_error'] = "email is required!!"
                if not is_valid_email(email):
                    valid_error['valid_email_error'] = "enter correct email format!!"
                
                if not password:
                    empty_error['empty_password_error'] = "password is required!!"
                
                if not empty_error and not valid_error:
                    try:
                        user = user_registration.objects.get(email=email, is_active=True)
                    except user_registration.DoesNotExist:
                        user = None
                        try:
                            if user_registration.objects.get(email=email):
                                valid_error['deactivated'] = "Your account is Deactive!!"
                                user = 'deactive'
                        except user_registration.DoesNotExist:
                            user=None
                

                        
                    # Check if the user exists and the password matches
                    if user and check_password(password, user.password):
                        request.session['user_id'] = user.user_id
                        request.session['username'] = user.username
                        active = "active"
                        request.session['active_user'] = active
                        request.session.set_expiry(3600)
                        if try_to_checkout:
                            image = upload_images.objects.get(image_id=try_to_checkout)
                            if image.user==user:
                                notification_centre.objects.create(
                                user = user,
                                event_type = 'login',
                                message = "Last login: ",
                                )
                                return redirect('profile_page')
                            else:
                                notification_centre.objects.create(
                                user = user,
                                event_type = 'login',
                                message = "Last login: ",
                                )
                                return redirect(reverse('checkout', kwargs={'image_id': try_to_checkout}))

                        else:
                            notification_centre.objects.create(
                                user = user,
                                event_type = 'login',
                                message = "Last login: ",
                            )
                            return redirect('profile_page')
                        
                    
                    else:
                        valid_error['email_password_invalid'] = "invalid email or password!!"


        return render(request, 'login.html', {'empty_error':empty_error, 'valid_error':valid_error})


def forgot_password(request):
    valid_error={}
    change_error={}
    is_active = request.session.get('active_user')
    user_id = request.session.get('user_id')
    if is_active and user_id:
        return redirect('profile_page')

    else:
        
        if request.method=="POST":
            if 'send_otp' in request.POST:
                email = request.POST.get('email')
                if not email:
                    valid_error['email_empty'] = "Email field is required!!"
                if not is_valid_email(email):
                    valid_error['email_invalid'] = "Enter correct email format!!"   

                if not valid_error:
                    try:
                        user = user_registration.objects.get(email=email, is_active=True)
                    except user_registration.DoesNotExist:
                        user = None
                        if user_registration.objects.get(email=email):
                            valid_error['user_active'] = "User account is deactive!!"

                    if not user:
                        valid_error['user_exist'] = "User doesn't exists!!"

                    if user:
                        

                        last_otp_sent_time = request.session.get('last_otp_sent_time', 0)
                        current_time = time.time()

                        if (last_otp_sent_time == 0) or (current_time - last_otp_sent_time) >= 55:
                            otp_code = ''.join(random.choices('0123456789', k=6))
                            # print(otp_code)

                            send_mail(
                                'Your OTP for email verification',
                                f'OTP code for reseting password: {otp_code}',
                                'project020g@gmail.com',
                                [email],
                                fail_silently=False
                            )
                            request.session['reset_user'] = user.user_id
                            request.session['otp_code'] = otp_code
                            request.session['last_otp_sent_time'] = time.time()
                            request.session.set_expiry(600)
                            timer = 60    
                        else:
                           valid_error['resend_otp'] = "Resend otp after 60 seconde!!"

            if 'change_password' in request.POST:
                if not request.session.get('reset_user'):
                    change_error['send_otp_first'] = "Send OTP first to reset!!"
                elif request.session.get('reset_user'):
                    actual_otp = request.session.get('otp_code') 
                    entered_otp = request.POST.get('otp')
                    new_password = request.POST.get('new_password')
                    confirm_password = request.POST.get('confirm_password')
                    user_id = request.session.get('reset_user')
                    try:
                        user = user_registration.objects.get(user_id=user_id, is_active=True)
                    except user_registration.DoesNotExist:
                        user = None

                    if not entered_otp:
                        change_error['otp_empty'] = "Enter OTP code!!"
                    if len(new_password) < 6:
                        change_error['pass_length'] = "Password must be of atleast 6 length!!"
                    if new_password != confirm_password:
                        change_error['pass_match'] = "Both password must match!!"   
                    if actual_otp != entered_otp:
                        change_error['otp_match'] = "Enter correct OTP!!"
                    if not change_error and user:
                        user.password = make_password(new_password)
                        user.save()
                        notification_centre.objects.create(
                                user = user,
                                event_type = 'password_reset',
                                message = "Your password was reset successfully!! ",
                            )
                        request.session.flush()
                        return redirect('user_login')

    return render (request, 'forgot_password.html', {'valid_error': valid_error, 'change_error':change_error})