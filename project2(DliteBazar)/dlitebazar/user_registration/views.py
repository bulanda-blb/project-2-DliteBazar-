from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import user_registration
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from profile_dashboard.models import notification_centre
import random
import time
import re
from django.core.mail import send_mail


def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)

def is_valid_name(name):
    name_regex = r'^[a-zA-Z\s]+$'
    return re.match(name_regex, name)


def generate_unique_username(first_name):
    base_username = first_name.lower()
    while True:
        random_suffix = random.randint(100, 999)  # Generate a random three-digit number
        unique_username = f"{base_username}{random_suffix}"
        if not user_registration.objects.filter(username=unique_username).exists():
            return unique_username

    

def register_user(request):
    if(request.session.get('registration_data')):
        return redirect('email_verification')
    validation_error = {}
    registration_data = {}
    
    if request.method == 'POST':
        request.session.flush()

        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        npassword = request.POST.get('npassword')
        cpassword = request.POST.get('cpassword')

        

        if not firstname:
            validation_error['firstname_error_empty'] = "first name is required!!"
        elif not is_valid_name(firstname):
            validation_error['firstname_error_valid'] = "first name only contains characters!!"

        if middlename and not is_valid_name(middlename):
            validation_error['middlename_error_valid'] = "middle name only contains character!!"

        if not lastname:
            validation_error['lastname_error_empty'] = "last name is required!!"
        elif not is_valid_name(lastname):
            validation_error['lastname_error_valid'] = "last name only contains characters!!" 

        if not email:
            validation_error['email_error_empty'] = "email is requied!!"
        elif not is_valid_email(email):
            validation_error['email_error_valid'] = "enter correct email format!!"
        elif user_registration.objects.filter(email=email).exists():
            validation_error['email_error_exist'] = "email already registered!!"

        if not npassword:
            validation_error['password_error_empty'] = "password is required!!"
        elif len(npassword) < 6:
            validation_error['password_error_length'] = "password must be atleast 6 characters long!!"

        if npassword != cpassword:
            validation_error['password_error_match'] = "password did't match!!"

        if not validation_error:
            # Storing form data in session
            request.session['registration_data'] = {
            'firstname': firstname,
            'middlename': middlename,
            'lastname': lastname,
            'email': email,
            'username': generate_unique_username(firstname),
            'password': make_password(npassword),
            }
            request.session.set_expiry(360)
            return redirect('email_verification')
        else:
            registration_data = {
                'firstname': firstname,
                'middlename': middlename,
                'lastname': lastname,
                'email': email,
                'npassword': npassword,
                'cpassword': cpassword,
            }
            
        
        


    return render(request, 'register.html', {'validation_error':validation_error, 'registration_data':registration_data})


def email_verification(request):
    error_message = None
    valid_otp_code = None
    timer = None
    registration_data = request.session.get('registration_data')

    if request.method == 'POST':
        if 'send_otp' in request.POST:
            last_otp_sent_time = request.session.get('last_otp_sent_time', 0)
            current_time = time.time()

            if (last_otp_sent_time == 0) or (current_time - last_otp_sent_time) >= 55:
                otp_code = ''.join(random.choices('0123456789', k=6))
                # print(otp_code)
                email = registration_data.get('email')

                send_mail(
                    'Your OTP for email verification',
                    f'OTP code: {otp_code}',
                    'project020g@gmail.com',
                    [email],
                    fail_silently=False
                )
                request.session['otp_code'] = otp_code
                request.session['last_otp_sent_time'] = time.time()
                timer = 60

            return render(request, 'email_verification.html', {'timer': timer, 'registration_data': registration_data})

        elif 'send' in request.POST:
            submitted_otp_code = request.POST.get('otp_code')
            generated_otp_code = request.session.get('otp_code')
            if submitted_otp_code == generated_otp_code:
                user_data = user_registration.objects.create(
                    first_name=registration_data.get('firstname'),
                    middle_name=registration_data.get('middlename'),
                    last_name=registration_data.get('lastname'),
                    email=registration_data.get('email'),
                    password=registration_data.get('password'),
                    username=registration_data.get('username'),
                    date_joined=timezone.now(),
                )
                user_registered = user_registration.objects.get(username=registration_data.get('username'))
                notification_centre.objects.create(
                    user = user_registered,
                    event_type = 'registration',
                    message = f"Account created successfully!! with verified email {registration_data.get('email')}"
                )

                
                email = registration_data.get('email')
                send_mail(
                    'Your OTP for email verification',
                    f'Your account registration is successfull!!',
                    'project020g@gmail.com',
                    [email],
                    fail_silently=False
                )
                request.session.flush()
                return redirect('user_login')
            else:
                valid_otp_code = "Please enter a valid OTP code"

        elif 'edit' in request.POST:
            edited_data = {
                'firstname': request.POST.get('firstname'),
                'middlename': request.POST.get('middlename'),
                'lastname': request.POST.get('lastname'),
                'email': request.POST.get('email'),
            }
            # Update session data with edited values
            registration_data.update(edited_data)
            request.session['registration_data'] = registration_data

    return render(request, 'email_verification.html', {'registration_data': registration_data, 'error_message': error_message, 'valid_otp_code': valid_otp_code, 'timer': timer})




