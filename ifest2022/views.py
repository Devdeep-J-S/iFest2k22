from locale import currency
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime, AdminTimeWidget
import json
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from .models import *
from .forms import *

# Create your views here.

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def welcome(request):
    return redirect('home')

def home(request):
    return render(request, 'home.html')

def pronites(request):
    return render(request, 'pronites.html')

def speakers(request):
    return render(request,'speakers.html')

def ifestTeam(request):
    return render(request,'members.html')

def sponsors(request):
    return render(request,'sponsors.html')

def login_func(request):
    if request.user.is_anonymous==False:
        return redirect('profile')
    if request.method == 'POST':
        #username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.profile.payment == 0:
                if user.profile.referral_code:
                    CA = campusAmbassador.objects.filter(referralCode=user.profile.referral_code)
                    newCount = CA[0].count - 1
                    CA.update(
                        count=newCount,
                    )
                user.delete()
                messages.info(request,'Re-register and pay to login.')
                return redirect("login_page")
            else:
                login(request, user)
                return redirect('profile')
        else:
            messages.error(request, 'Username or password is incorrect.')
            return redirect('login_page')
    else :
        return render(request, 'registration/login.html')

def logout_func(request):
    logout(request)
    return redirect('home')


#def register(request):
#    currency = 'INR'
#    amount = 20000  # Rs. 200

    # Create a Razorpay Order
#    razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                       currency=currency,
#                                                       payment_capture='0'))

    # order id of newly created order.
#    razorpay_order_id = razorpay_order['id']
#    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
#    context = {}
#    context['razorpay_order_id'] = razorpay_order_id
#    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#    context['razorpay_amount'] = amount
#    context['currency'] = currency
#    context['callback_url'] = callback_url

#    return render(request, 'register.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': signature
            }
            #print(params_dict)
            userProfile = Profile.objects.get(order_id=razorpay_order_id).user
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            #print(result)
            if result is None:
                amount = 10000  # Rs. 100
                #if userProfile.email.find("@daiict.ac.in")!=-1:
                #    if userProfile.profile.ieee_id :
                #        amount = 5000 # Rs. 50
                #    else :
                #        amount = 10000  # Rs. 100
                if userProfile.profile.ieee_id:
                    amount = 5000 # Rs. 50
                try:
                    # capture the payment
                    razorpay_client.payment.capture(razorpay_payment_id, amount)
                    userProfile.refresh_from_db()
                    userProfile.profile.payment = 1
                    userProfile.profile.payment_id = razorpay_payment_id
                    #print(userProfile.profile.payment)
                    userProfile.save()
                    # render success page on successful capture of payment
                    messages.success(request, 'Payment Successful')
                    return redirect('login_page')
                except:
                    # if there is an error while capturing payment.
                    if userProfile.profile.referral_code:
                        CA = campusAmbassador.objects.filter(referralCode=userProfile.profile.referral_code)
                        newCount = CA[0].count - 1
                        CA.update(
                            count=newCount,
                        )
                    userProfile.delete()
                    messages.error(request, "Payment Failed")
                    return redirect('signup')
            else:
                # if signature verification fails.
                if userProfile.profile.referral_code:
                    CA = campusAmbassador.objects.filter(referralCode=userProfile.profile.referral_code)
                    newCount = CA[0].count - 1
                    CA.update(
                        count=newCount,
                    )
                userProfile.delete()
                messages.error(request, "Payment Failed")
                return redirect('signup')
        except:
            # if we don't find the required parameters in POST data
            username = request.GET.get('username')
            #print(username)
            userProfile = User.objects.get(username=username)
            if userProfile.profile.referral_code:
                CA = campusAmbassador.objects.filter(referralCode=userProfile.profile.referral_code)
                newCount = CA[0].count - 1
                CA.update(
                    count=newCount,
                )
            userProfile.delete()
            return redirect('home')
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()


def signup(request):
    # if request.user.is_anonymous == False:
    #     return redirect('profile')
    if request.method == "POST":
        form = CreateUserForm(request.POST or None)
        email = request.POST['email']
        ieee_id = request.POST['ieee_id']
        currency = 'INR'
        if User.objects.filter(email=request.POST['email']).exists():
            messages.error(request, "The email you entered is already registered.")
            return redirect('signup')
        
        if request.POST['password1'] != request.POST['password2']:
            messages.error(request, "The passwords entered do not match.")
            return redirect('signup')

        if request.POST['ieee_id']:
            if Profile.objects.filter(ieee_id=request.POST['ieee_id']).exists():
                messages.error(request, "The IEEE ID you entered is already registered.")
                return redirect('signup')
        if request.POST['referral_code']:
            if not campusAmbassador.objects.filter(referral_code=request.POST['referral_code']).exists():
                messages.error(request, "The referral code you entered is incorrect")
                return redirect('signup')
        CA = campusAmbassador.objects.filter(referral_code=request.POST['referral_code'])
        
        # Staff Authentication for Cash Payment
        staffUsername = request.POST['staff_username']
        staffPass = request.POST['staff_pass']

        staffUser = authenticate(request, username=staffUsername, password=staffPass)

        if staffUser is None or (not staffUser.is_staff):
            messages.error(request, "Staff Authentication failed.")
            return redirect('signup')

        if form.is_valid():
            if CA:
                newCount = CA[0].count + 1
                CA.update(
                    count=newCount,
                )
            user = form.save()
            user.refresh_from_db()
            user.username = user.email
            user.profile.university = form.cleaned_data.get('university')
            user.profile.contact_number = form.cleaned_data.get('contact_number')
            user.profile.ieee_id = form.cleaned_data.get('ieee_id')
            user.profile.referral_code = form.cleaned_data.get('referral_code')
            user.profile.payment = True     # Is payment done ?
            user.profile.staffAuth = staffUser.get_full_name()
            user.save()
            return redirect('home')

    form = CreateUserForm()
    return render(request, "signup22.html", {'form':form})


# def signup(request):
#     if request.user.is_anonymous==False:
#         return redirect('profile')
#     form = CreateUserForm()
#     if request.method == "POST":
#         form = CreateUserForm(request.POST or None)
#         email = request.POST['email']
#         ieee_id = request.POST['ieee_id']
#         currency = 'INR'
#         amount = 10000  # Rs. 100
#         #if email.find("@daiict.ac.in") != -1:
#         #    if ieee_id:
#         #        amount = 5000 # Rs. 50
#         #    else:
#         #        amount = 10000  # Rs. 100
#         if ieee_id:
#             amount = 5000 # Rs. 50
#         # Create a Razorpay Order
#         razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                            currency=currency,
#                                                            payment_capture='0'))
#         #print(razorpay_order)
#         # order id of newly created order.
#         razorpay_order_id = razorpay_order['id']
#         razorpay_order_status = razorpay_order['status']
#         #callback_url = 'paymenthandler/'
#         # we need to pass these details to frontend.
#         #context = {}
#         #context['razorpay_order_id'] = razorpay_order_id
#         #context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#         #context['razorpay_amount'] = amount
#         #context['currency'] = currency
#         #context['callback_url'] = callback_url
#         #context['form'] = form
#         #if User.objects.filter(username=request.POST['username']).exists():
#         #    messages.error(request, "The username you entered is already taken")
#         #    return redirect('signup')
#         if User.objects.filter(email=request.POST['email']).exists():
#             messages.error(request, "The email you entered is already registered")
#             return redirect('signup')
#         if request.POST['ieee_id']:
#             if Profile.objects.filter(ieee_id=request.POST['ieee_id']).exists():
#                 messages.error(request, "The IEEE ID you entered is already registered")
#                 return redirect('signup')
#         if request.POST['referral_code']:
#             if not campusAmbassador.objects.filter(referralCode=request.POST['referral_code']).exists():
#                 messages.error(request, "The referral code you entered is incorrect")
#                 return redirect('signup')
#         CA = campusAmbassador.objects.filter(referralCode=request.POST['referral_code'])
#         if form.is_valid():
#             if razorpay_order_status=='created':
#                 if CA:
#                     newCount = CA[0].count + 1
#                     CA.update(
#                         count=newCount,
#                     )
#                 form.save()
#                 user = form.save()
#                 user.refresh_from_db()  # load the profile instance created by the signal
#                 user.username = user.email
#                 #user.profile.DOB = form.cleaned_data.get('DOB')
#                 user.profile.university = form.cleaned_data.get('university')
#                 user.profile.contact_number = form.cleaned_data.get('contact_number')
#                 user.profile.ieee_id = form.cleaned_data.get('ieee_id')
#                 user.profile.referral_code = form.cleaned_data.get('referral_code')
#                 user.profile.payment = 0
#                 user.profile.order_id = razorpay_order_id
#                 user.save()
#                 #print(user)
#                 username = form.cleaned_data['email']
#                 razorpay_order['name'] = username
#                 #print(razorpay_order)
#                 return render(request, "register.html", {
#                     'userProfile': user,
#                     'payment': razorpay_order,
#                     #'callback_url': callback_url,
#                     'razor_key_id': settings.RAZOR_KEY_ID,
#                 })
#                 #messages.success(request, 'Account was created for ' + username)
#                 #return render(request, "registration/signup.html", {'form': form, 'payment':razorpay_order})
#                 #return redirect("login_page")
#                 #return redirect("register")
#         else:
#             messages.error(request, "Invalid form entries.")
#             return redirect('signup')
#     else:
#         return render(request, "registration/signup.html", {'form':form})


def events(request):
    events = Event.objects.all()
    return render(request,'events.html',{"events": events})

@login_required(login_url='login_page')
def dashboard(request):
    registrations = Registration.objects.filter(userProfile=request.user)
    events = []
    for registration in registrations:
        events.append(registration.event)
    if events:
        return render(request,'events.html',{"events":events,
                                             "dashboard": "1"})
    else:
        return render(request,'events.html',{"dashboard": "1"})

def moreInfo(request):
    user = request.user
    event_id = request.GET.get('id')
    event = Event.objects.filter(id=event_id)
    if request.user.is_anonymous==False:
        registration = Registration.objects.filter(userProfile=user).filter(event=event[0])
        flag = 0
        if registration:
            flag = 1
        if request.method == 'GET':
            now = datetime.datetime.now()
            if flag:
                return render(request, 'moreInfo.html', {
                    "event": event[0],
                    "now": now,
                    "button": 'De-register',
                    "links": "links",
                })
            else:
                return render(request,'moreInfo.html', {
                    "event": event[0],
                    "now": now,
                    "button": 'Register',
                })
        else:
            if flag == 0:
                #if (event[0].paid==1 and user.profile.payment==1) or event[0].paid==0 :
                if user.profile.payment==1:
                    new_registration = Registration.objects.create(
                        userProfile = user,
                        event = event[0],
                    )
                    new_registration.save()
                    messages.success(request,f"You have successfully registered for {event[0].name}.")
                    return redirect('events')
                else:
                    user.delete()
                    return redirect('login_page')
            else:
                registration.delete()
                messages.success(request, f"You have de-registered from {event[0].name}.")
                return redirect('dashboard')
    else:
        now = datetime.datetime.now()
        return render(request, 'moreInfo.html', {
            "event": event[0],
            "now": now,
            "button": 'Register',
        })


@login_required(login_url='login_page')
def profile(request):
    return render(request,'profile.html')

@login_required(login_url='login_page')
def editProfile(request):
    user_id = request.user.id
    user = User.objects.filter(id=user_id)
    form = UpdateUserForm(initial={
        'first_name': user[0].first_name,
        #'last_name': user[0].last_name,
        #'DOB': user[0].profile.DOB,
        'university': user[0].profile.university,
        'contact_number': user[0].profile.contact_number,
    })
    if request.method == 'GET':
        return render(request, 'editProfile.html', {
            'form': form
        })
    else:
        form = UpdateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data.get('first_name')
            #last_name = form.cleaned_data.get('last_name')
            #DOB = form.cleaned_data.get('DOB')
            university = form.cleaned_data.get('university')
            contact_number = form.cleaned_data.get('contact_number')
            user.first_name = first_name
            #user.last_name = last_name
            #user.profile.DOB = DOB
            user.profile.university = university
            user.profile.contact_number = contact_number
            user.save()
            return redirect('profile')
        else:
            messages.error(request, "Invalid form entries.")
            return redirect('editProfile')





