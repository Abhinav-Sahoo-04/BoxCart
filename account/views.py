from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# User Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
def login(request):
    if request.method=="POST":    
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(username=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid Username and passeword !")
            return redirect('login')
        
    return render(request,'account/login.html')

def register(request):
    registed_success=False
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username)
            user.phone_number=phone_number
            user.set_password(password)
            user.save()
            # USER verification
            current_site=get_current_site(request)
            mail_subject="Activate your account"
            message=render_to_string('account/account_verification_email.html',{
                "user":user,
                "domain":current_site,
                "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                "token":default_token_generator.make_token(user),
            })
            to_mail=email
            send_mail=EmailMessage(mail_subject,message,to=[to_mail])
            send_mail.send()
            # messages.success(request,"Registration was successful !")
            return redirect('/account/login/?command=verification&email='+email)
    else:
        form=RegistrationForm()
    context={
        'form':form,
        "registed_success":registed_success,
    }
    return render(request,'account/register.html',context)
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out")
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Congratulation ! Your account is activated .")
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('register')
