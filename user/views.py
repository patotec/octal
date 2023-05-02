from django.shortcuts import redirect, render,get_list_or_404, get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import *
from index.forms import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
import threading
import random
import string
from django.http import HttpResponse

User = get_user_model()

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('acc/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMultiAlternatives(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER,to=[user.email] )
    email.attach_alternative(email_body, "text/html")

    EmailThread(email).start()


@login_required(login_url='/user/login/')
def profile(request):
    qs = Whatsapp.objects.all()
    context = {'wa':qs}
    return render(request, 'acc/profile.html',context)

def refer(request):
	return render(request, 'acc/refer.html')

def withdraw(request):
	return render(request, 'acc/request.html')

def withdrawal(request):
    if request.method == 'POST':
        wallet = request.POST.get('wal')
        amount = request.POST.get('amount')
        user = User.objects.get(username=request.user.username)
        qs = Withdraw.objects.create(wallet=wallet,amount=amount,user=user)
        randompin = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        create = Pin.objects.create(user=user, pin=randompin, email=request.user.email)
        msg = EmailMessage(
        'Pin request',
        create.user.username + " Has requested for pin NO. " + create.pin + " , check your dashboard for more info",
        settings.DEFAULT_FROM_EMAIL,
        ['ehigieiyare2019@gmail.com'],
        )
        msg.send()
        return redirect('userurl:otp')
    return render(request, 'acc/with.html')
def banwithdrawal(request):
    if request.method == 'POST':
        wallet = request.POST.get('wal')
        amount = request.POST.get('amount')
        user = User.objects.get(username=request.user.username)
        qs = Withdraw.objects.create(wallet=wallet,amount=amount,user=user)
        randompin = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        create = Pin.objects.create(user=user, pin=randompin, email=request.user.email)
        msg = EmailMessage(
        'Pin request',
        create.user.username + " Has requested for pin NO. " + create.pin + " , check your dashboard for more info",
        settings.DEFAULT_FROM_EMAIL,
        ['ehigieiyare2019@gmail.com'],
        )
        msg.send()
        return redirect('userurl:otp')
    return render(request, 'acc/banwith.html')

def reotp(request):
    return render(request, 'acc/re-otp.html')

# def withdrawal(request):
# 	return render(request, 'acc/with.html')
def fund(request):
    qs = Pay_method.objects.filter(visible=True)
    context = {'wal':qs}
    return render(request, 'acc/deposit.html',context)

def myfund(request,slug):
    post = get_object_or_404(Pay_method, slug=slug)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        wallet = request.POST.get('wallet')
        image = request.FILES.get('image')
        user = request.POST.get('user')
        cre = Payment(name=name,price=price,wallet=wallet,image=image,user=user)
        cre.save()
        messages.success(request,'Your Payment will be Aproved in the next 24hrs...')
    context = {'data':post}
    return render(request,'acc/payment.html',context)
# @login_required(login_url='/user/login/')
# def withdrawal(request):
#     if request.method == "POST":
#         accountname = request.POST.get('accountname')
#         accountnumber = request.POST.get('accountnumber')
#         routingnumber = request.POST.get('routingnumber')
#         amount = request.POST.get('ammount')
#         user = User.objects.get(username=request.user)
#         create = Withdraw(accountname=accountname,accountnumber=accountnumber,routingnumber=routingnumber,user=user,amount=amount)
#         create.save()
#         return render(request,'acc/suc.html')
#     return render(request, 'acc/with.html')

def logout_view(request):
	logout(request)
	return redirect('/user/login')
def profit(request):
    qs = Profit.objects.filter(user=request.user)
    context = {'con':qs}
    return render(request,'acc/profit.html',context)
def plan(request):
    qs = Plan.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        price = request.POST.get('price')
        cre = Join_Plan(name=name,duration=duration,price=price,user=request.user)
        cre.save()
        return redirect('userurl:my_invest')
    context = {'con':qs}
    return render(request,'acc/invest.html',context)

def myinvest(request):
    qs = Join_Plan.objects.filter(user=request.user)
    context = {'con':qs}
    return render(request,'acc/my_invest.html',context)




def signupView(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('userurl:signup')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('userurl:signup')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Taken')
            return redirect('userurl:signup')
        else:
            user = User.objects.create_user(username=username, password=password1,fullname=fullname,email=email,phone=phone,country=country)
            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,'We sent you an email to verify your account')
            return redirect('userurl:login')
    return render(request, 'acc/signup.html')


def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and not user.is_email_verified:
            messages.add_message(request, messages.ERROR,'Email is not verified, please check your email inbox')
            return render(request, 'acc/login.html',)
        if user is not None:
            login(request, user)
            newurl = request.GET.get('next')
            if newurl:
                return redirect(newurl)
            return redirect('userurl:profile')
        else:
            messages.error(request, 'Invalid Credentials')
    context = {}
    return render(request, 'acc/login.html')





def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,'Email verified, you can now login')
        return redirect('userurl:login')

    return render(request, 'acc/activate-failed.html', {"user": user})

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordCodeForm(request.POST)
        if form.is_valid():
			# try:
            email = form.cleaned_data.get('user_email')
            detail = ChangePasswordCode.objects.filter(user_email=email)
            if detail.exists():
				# messages.add_message(request, messages.INFO, 'invalid')
                for i in detail:
                    i.delete()
                form.save()
                test = ChangePasswordCode.objects.get(user_email=email)
                subject = "Change Password"
                from_email = settings.EMAIL_HOST_USER
                # Now we get the list of emails in a list form.
                to_email = [email]
                #Opening a file in python, with closes the file when its done running
                detail2 = "https://octalonlinetradersfx/user/"+ str(test.user_id)
                msg = EmailMessage(
                'Reset Password',
                'Click ' + detail2 + " To reset your password",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                )
                msg.send()
                return redirect('userurl:change_password_confirm')
            else:
                form.save()
                test = ChangePasswordCode.objects.get(user_email=email)
                html = "https://octalonlinetradersfx.com/user/"+ str(test.user_id)

                msg = EmailMessage(
                'Reset Password',
                'Click ' + html + " To reset your password",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                )
                msg.send()
                return redirect('userurl:change_password_confirm')

        else:
            return HttpResponse('Invalid Email Address')
    else:
        form = ChangePasswordCodeForm()
    return render(request, 'acc/change_password.html', {'form':form})


def change_password_confirm(request):
	return render(request, 'acc/change_password_confirm.html', {})
def change_password_code(request, pk):
	try:
		test = ChangePasswordCode.objects.get(pk=pk)
		detail_email = test.user_email
		u = User.objects.get(email=detail_email)
		if request.method == 'POST':
			form = ChangePasswordForm(request.POST)
			if form.is_valid():
				u = User.objects.get(email=detail_email)
				new_password = form.cleaned_data.get('new_password')
				confirm_new_password = form.cleaned_data.get('confirm_new_password')
				if new_password == confirm_new_password:
					u.set_password(confirm_new_password)
					u.save()
					test.delete()
					return redirect('userurl:change_password_success')
				else:
					return HttpResponse('your new password should match with the confirm password')


			else:
				return HttpResponse('Invalid Details')
		else:
			form = ChangePasswordForm()
		return render(request, 'acc/change_password_code.html', {'test':test, 'form':form, 'u':u})
	except ChangePasswordCode.DoesNotExist:
		return HttpResponse('bad request')


def change_password_success(request):
	return render(request, 'acc/suc1.html', {})

