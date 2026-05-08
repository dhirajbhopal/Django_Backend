from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from core.forms import SignUpForm, ProfileForm,ImgForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from django.views import View
from core.models import User,UniqueCode,donation,UserLoginInfo,updates
from .models import UserLoginInfo
from django.conf import settings
from django.contrib import messages
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint
from django.conf import settings 
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from PIL import Image
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile
# upi Payennet down
from urllib.parse import urlencode
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from .utils import build_upi_deeplink
from io import BytesIO
import qrcode
# Password reset 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db.models import Sum
from .models import UniqueCode
import random
import string

# user loaction
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .utils import get_client_ip, get_geo_info, get_device_info
from datetime import datetime


class ProfileView(View):
    if User.is_authenticated:
        def get(self, request):
            form = ProfileForm(request.POST)
            return render(request,'commons/profile.html',{'form':form})

class ProfileUpdate(UpdateView):
    if User.is_authenticated:
        model = User
        form_class = ProfileForm
        success_url = reverse_lazy('home')
        template_name = 'commons/profile.html'

class Imageview(View):
    if User.is_authenticated:
        def get(self, request):
            form = ImgForm(request.POST)
            return render(request,'commons/imageupdate.html',{'form':form})

class mysingup(View):

    def get(self,request):
        try:
            return render(request,'commons/signup.html')
        except Exception as ex:
            msg="signup form not found"
            return render(request,'base.html',{'msg':msg})


from django.core.files.base import ContentFile
from django.shortcuts import redirect

@login_required
def Imageupdate(req):
    try:
        email = req.POST.get("email")
        user = User.objects.get(email=email)

        # ---- DELETE OLD IMAGE ----
        if user.image:
            if os.path.isfile(user.image.path):
                os.remove(user.image.path)

        new_image = None

        # =========================
        # 1️⃣ CASE: FILE UPLOAD
        # =========================
        if 'image' in req.FILES:
            new_image = req.FILES['image']

        # =========================
        # 2️⃣ CASE: CAMERA (BASE64)
        # =========================
        elif req.POST.get("image_data"):
            image_data = req.POST.get("image_data")

            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            new_image = ContentFile(
                base64.b64decode(imgstr),
                name=f"user_{user.id}.{ext}"
            )

        # =========================
        # SAVE IMAGE
        # =========================
        if new_image:
            user.image = new_image
            user.save()
            messages.success(req, "Profile photo updated successfully")
        else:
            messages.error(req, "No image selected")

        return redirect('/')

    except Exception as ex:
        print("Error while updating image:", ex)
        messages.error(req, "Something went wrong while updating image")
        return redirect('/')

class forgotpassword(View):

    def get(self,request):
        return render(request,'commons/forgotpass.html')

class signuptask(View):

    def get(self,request):
        code = 0
        try:
            encryptedpassword=make_password(request.GET['password'])
            global emailuser
            emailuser = request.GET.get("emailid")
            ob=User()
            ob.username=request.GET.get("username")
            ob.mobileno=request.GET.get("mobileno")
            ob.email=request.GET.get("emailid")
            ob.first_name=request.GET.get("name")
            ob.last_name=request.GET.get("name1")
            ob.password=encryptedpassword
            ob.gender=request.GET.get("gender")
            ob.address=request.GET.get("address")
            ob.save()
        except IntegrityError as ex:          
            code = 1
            messages.success(request,'Email is Already Registered! need to reset password')
            return redirect('login')
        except Exception as ex:       
            code = 2
            messages.success(request,'Email id does not exist !')
            return render(request,'commons/signup.html')
        return redirect("/cheksignup?err="+str(code))


def cheksignup(req):
    code = req.GET.get("err")
    msg = ""
    if code=="0":
        message ="""<html><body><h1 style='color:red'>PATEL JAN KALYAN SEVA SAMITI</h1> <hr>Hello Mr. Dhiraj Patel Admin <br><br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        One New User has registered, Please assign his/her Role and Roll No. <b><br>
        User Eamil id is:- """+emailuser+"""<br><br>
        Visit :- <span style='color:red'> https://pjkss.com/pateladminlogin/?next=/pateladminlogin </spna> </b> to login <br>
        <br><b> Thanks<br><br> Patel Jan Kalyan Seva Samiti <br>  Head Office Dehri </b></body></html>"""
        smtp = smtplib.SMTP(host='smtp.gmail.com', port=587)
        smtp.starttls()
        smtp.login("pjkssinfo@gmail.com","bwqpbkcdutyqheoi")
        msg = MIMEMultipart() 
        msg['From'] ="PJKSS ADMIN"
        msg['To'] = "dhirajpatel08@gmail.com"
        msg['Subject'] = "New Registeration"
        msg.attach(MIMEText(message, 'html'))
        smtp.send_message(msg)
        smtp.quit()
        message ="""<html><body><h1 style='color:red'>PATEL JAN KALYAN SEVA SAMITI</h1> <hr>Hello Mr. """+emailuser+""" <br><br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Your Registration is Successfull <b><br>
        Your User id is:- """+emailuser+"""<br><br>
        Visit :- <span style='color:red'> https://pjkss.com/login </spna> </b> to login <br>
        <br><b> Thanks<br><br> Patel Jan Kalyan Seva Samiti <br>  Head Office Dehri </b></body></html>"""
        smtp = smtplib.SMTP(host='smtp.gmail.com', port=587)
        smtp.starttls()
        smtp.login("pjkssinfo@gmail.com","bwqpbkcdutyqheoi")
        msg = MIMEMultipart() 
        msg['From'] ="PJKSS ADMIN"
        msg['To'] = emailuser
        msg['Subject'] = "Registration is Successfull"
        msg.attach(MIMEText(message, 'html'))
        smtp.send_message(msg)
        smtp.quit()
        messages.success(req,"Registeration Done Successfully")
        return redirect('login')
    if code=="1":
        messages.success(req,'Email is Already Registered !')      
    if code=="2":
        messages.success(req,'Registeration Failed !')     
    return render(req,'commons/signup.html')

def generateOTP(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def sendmail(email,otp):
    try:
        print("mail iniitializing")
        message ="""<html><body><h1 style='color:red'>PATEL JAN KALYAN SEVA SAMITI</h1> <hr>Hello Mr. {0},<br><br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Please enter otp to complete your registration <b><br><br>
        Your OTP is :-<span style='color:red'>  {1} </spna> </b> please don't share to anyone.<br>
        <br><b> Thanks<br><br> Patel Jan Kalyan Seva Samiti <br>  Head Office Dehri </b></body></html>""".format(email,otp)
        smtp = smtplib.SMTP(host='smtp.gmail.com', port=587)
        smtp.starttls()
        smtp.login("pjkssinfo@gmail.com","bwqpbkcdutyqheoi")
        msg = MIMEMultipart() 
        msg['From'] ="PJKSS ADMIN"
        msg['To'] = email
        msg['Subject'] = "Registration OTP"
        msg.attach(MIMEText(message, 'html'))
        smtp.send_message(msg)
        smtp.quit()     
        return True
    except Exception as ex:       
        return False


def sendotp(request):
    email = request.GET.get("email")
    print("your mail is+++++ ",email)
    if len(email)>0:
        email = email
        otp = generateOTP(6)
        print("your OTP is+++++ ",otp)
        check = sendmail(email,otp)
        print("sending mail+++++ ")
        request.session['loginotp'] = otp
        return HttpResponse("OTP Send Successfully! "+str(otp)+" ")
    else:
        return HttpResponse("OTP Send Failed, Please Try Again  !")           
                
    return HttpResponse("Email Id Not Exist !")



def forgotsendmail(email,otp):
    try:
        print("mail iniitializing")
        message ="""<html><body><h1 style='color:red'>PATEL JAN KALYAN SEVA SAMITI</h1> <hr>Hello Mr. {0},<br><br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Please enter otp to reset your password <b><br><br>
        Your OTP is :-<span style='color:red'>  {1} </spna> </b> please don't share to anyone.<br>
        <br><b> Thanks<br><br> Patel Jan Kalyan Seva Samiti <br>  Head Office Dehri </b></body></html>""".format(email,otp)
        smtp = smtplib.SMTP(host='smtp.gmail.com', port=587) 
        smtp.starttls()
        smtp.login("pjkssinfo@gmail.com","bwqpbkcdutyqheoi")
        msg = MIMEMultipart() 
        msg['From'] ="PJKSS ADMIN"
        msg['To'] = email
        msg['Subject'] = "Password reset OTP"
        msg.attach(MIMEText(message, 'html'))
        smtp.send_message(msg)
        smtp.quit()     
        return True
    except Exception as ex:       
        return False


def forgotsendotp(request):
    email = request.GET.get("email")
    print("your mail is+++++ ",email)
    if len(email)>0:
        email = email
        otp = generateOTP(6)
        print("your OTP is+++++ ",otp)
        check = forgotsendmail(email,otp)
        print("sending mail+++++ ")
        request.session['loginotp'] = otp
        return HttpResponse("OTP Send Successfully! "+str(otp)+" ")
    else:
        return HttpResponse("OTP Send Failed, Please Try Again  !")           
                
    return HttpResponse("Email Id Not Exist !")


def resetpass(req):
    try:
        email=req.POST.get("emailid1")
        print("converted email id",email)
        encryptedpassword=make_password(req.POST['password'])
        rpass=User.objects.get(email=email)
        rpass.password=encryptedpassword
        rpass.save()
        message ="""<html><body><h1 style='color:red'>PATEL JAN KALYAN SEVA SAMITI</h1> <hr>Hello Mr."""+email+""",<br><br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        You have successfuly reset your password <b><br><br>
        Visit :- <span style='color:red'> https://pjkss.com/login </spna> </b> to login <br>
        <br><b> Thanks<br><br> Patel Jan Kalyan Seva Samiti <br>  Head Office Dehri </b></body></html>"""
        smtp = smtplib.SMTP(host='smtp.gmail.com', port=587) 
        smtp.starttls()
        smtp.login("pjkssinfo@gmail.com","bwqpbkcdutyqheoi")
        msg = MIMEMultipart() 
        msg['From'] ="PJKSS ADMIN"
        msg['To'] = email
        msg['Subject'] = "Password reset Done"
        msg.attach(MIMEText(message, 'html'))
        smtp.send_message(msg)
        smtp.quit()
        messages.success(req,'Password Changed Successfully')
        return redirect('login')
    except Exception as ex:
        messages.success(req,'Sorry, Email id is not register with us')
        return redirect('login')


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required
def generate_unique_code(request):
    defaults="PJKSS"
    current_year = datetime.now().year

    def create_code():
        # Generates a random 10-character string with letters + digits
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    code = defaults+f"{current_year}"+create_code()
    while UniqueCode.objects.filter(code=code).exists():
        code = create_code()
    UniqueCode.objects.create(code=code)
    messages.success(request,f'Generted Serial No is:- {code}')
    #return JsonResponse({'unique_code': code})
    #return redirect('/addserialno', {}'unique_code': code})
    return redirect('/addserialno')


@login_required
def addserialno(req):
    return render(req,'adminrole/addserialno.html')


@login_required
def searchserialno(req):
    code=req.POST.get("serialno")
    serial=UniqueCode.objects.filter(code=code)
    for i in serial:
        if (i.code!=code):
            messages.success(req,"Serial No. Not Found")
            return render(req,'adminrole/searchserialno.html')   
        else:
            serial=UniqueCode.objects.filter(code=code)
            return render(req,'adminrole/searchserialno.html',{'serial':serial})   
    messages.success(req,"Serial No. Not Found")  
    return render(req,'adminrole/searchserialno.html')


@login_required
def searchserialnoall(req):
    serialall=UniqueCode.objects.all()
    return render(req,'adminrole/searchserialnoall.html',{'serialall':serialall})    






@login_required
def editserialno(req):
    try:
        if req.method=="GET":
            code=req.GET.get("serialno")
            serialdata=UniqueCode.objects.get(code=code)
            serialdata=UniqueCode.objects.filter(code=code)
            return render(req,'adminrole/editserialno.html',{'serialdata':serialdata})
        else:
            code=req.POST.get("serialno")
            modstu3=UniqueCode.objects.get(code=code)
            modstu3.issuedto=req.POST.get("issuedto")
            modstu3.subject=req.POST.get("subject")
            modstu3.issuedate=req.POST.get("issuedate")
            modstu3.issuername=req.POST.get("issuername")
            modstu3.save()
            messages.success(req,"Serial No Updated ") 
            return redirect('/searchserialno')
    except Exception as ex:
        messages.success(req,"Please fill corrcet Date ") 
        return redirect('/addserialno')


def gallery1(req):
    return render(req,'gallery1.html')


def gallery2(req):
    return render(req,'gallery2.html')

def gallery3(req):
    return render(req,'gallery3.html')

def donate(req):
    return render(req,'donate.html')


def donationdetail(request):
    if request.method=="POST":
        context = {}
        amount=request.POST.get("amount")
        qr_text = "upi://pay?pa=dhirajpatel08@okaxis&pn=DHIRAJ%20PATEL&am="+amount+"&cu=INR&aid=uGICAgID1xJq5DA"
        qr_image = qrcode.make(qr_text, box_size=15)
        qr_image_pil = qr_image.get_image()
        stream = BytesIO()
        qr_image_pil.save(stream, format='PNG')
        qr_image_data = stream.getvalue()
        qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
        context['qr_image_base64'] = qr_image_base64
        context['variable'] = qr_text
        upilinkPTM="https://mercury-uat.phonepe.com/transact/uat_v2?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVzT24iOjE3NjAxODUwMzU2MTUsIm1lcmNoYW50SWQiOiJNMjNEMExMSEpGSUZOIiwibWVyY2hhbnRPcmRlcklkIjoiT01QTDI1MTAxMTExMTcxNTYxMzUyODYwMTIifQ.smreWX7rPu8g6SJwVi3l9HpeINGHwAsR3zW2N_muEAA"
        return render(request,'site/donationqr.html',{'qr_image_base64':qr_image_base64,"upilinkPTM":upilinkPTM})
    else:
        return render(request,'site/donation.html')



def donationlist(req):
    donationdetails=donation.objects.all()
    total_amount = donationdetails.aggregate(total=Sum('Amount'))['total']
    return render(req,'member/donationlist.html',{'donationdetails':donationdetails, 'total_amount' :total_amount})


# user loaction
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    geo = get_geo_info(ip)
    device = get_device_info(request)

    UserLoginInfo.objects.create(
        user=user,
        ip_address=ip,
        city=geo.get('city'),
        region=geo.get('region'),
        country=geo.get('country'),
        browser=device.get('browser'),
        os=device.get('os'),
        device=device.get('device')
    )

def login_history(request):
    data = UserLoginInfo.objects.filter(user=request.user).order_by('-login_time')
    return render(request, 'tracker/login_history.html', {'data': data})



def publicsearch(req):
    return render(req,'site/publicserialno.html')

def publicsearchno(req):
    code=req.POST.get("serialno")
    serial=UniqueCode.objects.filter(code=code)
    for i in serial:
        if (i.code!=code):
            messages.success(req,"Serial No. Not Found")
            return render(req,'adminrole/searchserialno.html')   
        else:
            serial=UniqueCode.objects.filter(code=code)
            return render(req,'site/publicserialno.html',{'serial':serial})   
    messages.success(req,"Serial No. Not Found") 
    return render(req,'site/publicserialno.html')


def adminupdated(request):
    try:
        topicdata=topic()
        topicdata.topic=request.GET.get("topic")
        topicdata.date=request.GET.get("date")
        topicdata.save()
        messages.success(request,'Topic Updated Successfully')
        return redirect('/')
    except IntegrityError as ex:
        messages.success(request,'Fill data is not correct')
        return redirect('/')

class home(View):
    def get(self,request):
        dataupdate=updates.objects.all().order_by('-id')
        return render(request,'base.html',{'dataupdate':dataupdate})
        