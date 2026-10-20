from django.http import JsonResponse
from django.views import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from core.models import User, UniqueCode, donation, UserLoginInfo, updates
from django.contrib.auth.models import User
from rest_framework import serializers
from django.db.models import Sum
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .utils import get_client_ip, get_geo_info, get_device_info
import json
import os
import base64
import random
import string
import json
import smtplib
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import qrcode
from io import BytesIO
from rest_framework.views import APIView
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import (urlsafe_base64_encode,urlsafe_base64_decode)
from django.utils.encoding import force_bytes
from rest_framework import viewsets
#from .serializers import UserSerializer, UniqueCodeSerializer, donationSerializer , UserLoginInfoSerializer ,updatesSerializer
from django.db import IntegrityError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth import get_user_model
from datetime import datetime
from .serializers import UserLoginInfoSerializer

User = get_user_model()



# =========================================
# SIGNUP API
# =========================================

# ==========================================
# SIGNUP API
# ==========================================

@method_decorator(csrf_exempt, name='dispatch')
class Signup(View):

    def post(self, request):

        try:
            data = json.loads(request.body)

            email = data.get("email")

            # CHECK EMAIL EXISTS
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    "success": False,
                    "message": "Email already registered"
                }, status=400)

            # CREATE USER
            user = User.objects.create(
                username=data.get("username"),
                mobileno=data.get("mobileno"),
                email=email,
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                gender=data.get("gender"),
                address=data.get("address"),
                password=make_password(data.get("password"))
            )

            # =========================
            # ADMIN MAIL
            # =========================

            admin_message = f"""
            <html>
            <body>
            <h1 style='color:red'>
            PATEL JAN KALYAN SEVA SAMITI
            </h1>

            <hr>

            Hello Admin,<br><br>

            One New User has registered.<br><br>

            User Email :-
            <b>{email}</b>

            <br><br>

            Visit :
            <span style='color:red'>
            https://pjkss.com/pateladminlogin/?next=/pateladminlogin
            </span>

            <br><br>

            Thanks
            </body>
            </html>
            """

            smtp = smtplib.SMTP(
                host='smtp.gmail.com',
                port=587
            )

            smtp.starttls()

            smtp.login(
                "pjkssinfo@gmail.com",
                "bwqpbkcdutyqheoi"
            )

            msg = MIMEMultipart()

            msg['From'] = "PJKSS ADMIN"
            msg['To'] = "dhirajpatel08@gmail.com"
            msg['Subject'] = "New Registration"

            msg.attach(
                MIMEText(admin_message, 'html')
            )

            smtp.send_message(msg)

            smtp.quit()

            # =========================
            # USER SUCCESS MAIL
            # =========================

            user_message = f"""
            <html>
            <body>

            <h1 style='color:red'>
            PATEL JAN KALYAN SEVA SAMITI
            </h1>

            <hr>

            Hello {email},<br><br>

            Your Registration is Successful.<br><br>

            User ID :-
            <b>{email}</b>

            <br><br>

            Visit :
            <span style='color:red'>
            https://pjkss.com/login
            </span>

            <br><br>

            Thanks

            </body>
            </html>
            """

            smtp = smtplib.SMTP(
                host='smtp.gmail.com',
                port=587
            )

            smtp.starttls()

            smtp.login(
                "pjkssinfo@gmail.com",
                "bwqpbkcdutyqheoi"
            )

            msg = MIMEMultipart()

            msg['From'] = "PJKSS ADMIN"
            msg['To'] = email
            msg['Subject'] = "Registration Successful"

            msg.attach(
                MIMEText(user_message, 'html')
            )

            smtp.send_message(msg)

            smtp.quit()

            return JsonResponse({
                "success": True,
                "message": "Registration successful",
                "user_id": user.id
            }, status=201)

        except IntegrityError:

            return JsonResponse({
                "success": False,
                "message": "Email already exists"
            }, status=400)

        except Exception as e:

            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=500)


# ==========================================
# GENERATE OTP
# ==========================================

def generateOTP(n):

    range_start = 10 ** (n - 1)

    range_end = (10 ** n) - 1

    return random.randint(
        range_start,
        range_end
    )


# ==========================================
# SEND MAIL FUNCTION
# ==========================================

def sendmail(email, otp):

    try:

        message = f"""
        <html>
        <body>

        <h1 style='color:red'>
        PATEL JAN KALYAN SEVA SAMITI
        </h1>

        <hr>

        Hello {email},<br><br>

        Please enter OTP to complete registration.

        <br><br>

        Your OTP is :
        <span style='color:red'>
        {otp}
        </span>

        <br><br>

        Please don't share OTP with anyone.

        <br><br>

        Thanks

        </body>
        </html>
        """

        smtp = smtplib.SMTP(
            host='smtp.gmail.com',
            port=587
        )

        smtp.starttls()

        smtp.login(
            "pjkssinfo@gmail.com",
            "bwqpbkcdutyqheoi"
        )

        msg = MIMEMultipart()

        msg['From'] = "PJKSS ADMIN"
        msg['To'] = email
        msg['Subject'] = "Registration OTP"

        msg.attach(
            MIMEText(message, 'html')
        )

        smtp.send_message(msg)

        smtp.quit()

        return True

    except Exception as e:

        print(e)

        return False


# ==========================================
# SEND OTP API
# ==========================================

@csrf_exempt
def sendotp_api(request):

    if request.method != "POST":

        return JsonResponse({
            "success": False,
            "message": "POST method required"
        })

    try:

        data = json.loads(request.body)

        email = data.get("email")

        if not email:

            return JsonResponse({
                "success": False,
                "message": "Email required"
            })

        otp = generateOTP(6)

        check = sendmail(email, otp)

        if check:

            request.session['loginotp'] = otp

            return JsonResponse({
                "success": True,
                "message": "OTP Sent Successfully",
                "otp": otp
            })

        else:

            return JsonResponse({
                "success": False,
                "message": "OTP Sending Failed"
            })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        })
# =========================================
# LOGIN API
# =========================================
@csrf_exempt
def login_api(request):

    if request.method == "POST":

        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")

        try:

            user = User.objects.get(email=email)

            # CHECK PASSWORD
            if user.check_password(password):

                # VERY IMPORTANT
                user.backend = (
                    "django.contrib.auth.backends.ModelBackend"
                )

                # LOGIN SESSION
                login(request, user)

                return JsonResponse({
                    "success": True,
                    "message": "Login Successful",
                    "user": {
                        "id": user.id,
                        "role": user.role,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "mobileno": user.mobileno,
                        "gender": user.gender,
                        "address": user.address,
                        "image": str(user.image)
                                }
                })

            else:

                return JsonResponse({
                    "success": False,
                    "message": "Invalid Password"
                })

        except User.DoesNotExist:

            return JsonResponse({
                "success": False,
                "message": "Email Not Found"
            })

    return JsonResponse({
        "success": False
    })

# =========================================
# LOGOUT API
# =========================================

def logout_api(request):

    logout(request)

    return JsonResponse({
        "success": True,
        "message": "Logout successful"
    })


# =========================================
# PROFILE API
# =========================================

def profile_api(request):
    # 1. CHECK AUTHENTICATION
    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "User Not Logged In"
        }, status=401) # Explicit unauthorized status

    try:
        user = request.user

        # Safe image handling
        image_url = user.image.url if user.image else None
        # Note: If these fields are on a Profile model, use user.profile.mobileno, etc.

        return JsonResponse({
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "mobileno": getattr(user, 'mobileno', ''),
                "gender": getattr(user, 'gender', ''),
                "address": getattr(user, 'address', ''),
                "image": str(user.image)
            }
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Server Error: {str(e)}"
        }, status=500)


# =========================================
# UPDATE PROFILE API
# =========================================
@csrf_exempt
def update_profile_api(request):
    # 1. Ensure the user is actually logged in
    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "Authentication Required. Please log in."
        }, status=401)

    # 2. Only allow PUT requests
    if request.method != "PUT":
        return JsonResponse({
            "success": False,
            "message": "PUT Method Required"
        }, status=405)

    try:
        # Load the incoming React JSON data
        data = json.loads(request.body)

        # DYNAMIC USER: Get the user directly from the request session
        user = request.user

        # Update core user fields safely
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.mobileno = data.get("mobileno", user.mobileno)
        user.gender = data.get("gender", user.gender)
        user.address = data.get("address", user.address)

        # Save changes to the database
        user.save()

        return JsonResponse({
            "success": True,
            "message": "Profile Updated Successfully"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Server Error: {str(e)}"
        }, status=500)



# =========================================
# IMAGE UPLOAD API
# =========================================

@csrf_exempt
def imageupload(request):

    try:

        # USER ID
        user_id = request.POST.get("user_id")

        # IMAGE FILE
        image = request.FILES.get("image")

        if not user_id:

            return JsonResponse({
                "success": False,
                "message": "User ID missing"
            })

        if not image:

            return JsonResponse({
                "success": False,
                "message": "Image missing"
            })

        # GET USER
        user = User.objects.get(id=user_id)

        # DELETE OLD IMAGE
        if user.image:

            old_image_path = user.image.path

            if os.path.isfile(old_image_path):

                os.remove(old_image_path)

        # SAVE NEW IMAGE
        user.image = image

        user.save()

        return JsonResponse({

            "success": True,

            "message": "Image uploaded successfully",

            "image_url": user.image.url

        })

    except Exception as e:

        print(e)

        return JsonResponse({

            "success": False,

            "error": str(e)

        })


# =========================================
# API Profile data view
# =========================================

def profile_api(request):

    if not request.user.is_authenticated:

        return JsonResponse({
            "success": False,
            "message": "User Not Logged In"
        })

    user = request.user

    return JsonResponse({
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "mobileno": user.mobileno,
            "gender": user.gender,
            "address": user.address,
            "image": user.image.url if user.image else None
        }
    })

# =========================================
# GENERATE UNIQUE CODE API
# =========================================

@csrf_exempt
def generate_unique_code_api(request):
    defaults="PJKSS"
    def create_code():
        """Generates a random 10-character alphanumeric string."""
        return ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )

    # Get current year as string
    current_year = datetime.now().year  # e.g., 2026

    # Generate initial code with year included
    code = defaults+f"{current_year}"+create_code()

    # Ensure code is unique
    while UniqueCode.objects.filter(code=code).exists():
        #code = f"PJKSS{current_year}{create_code()}"
        code = defaults+f"{current_year}"+create_code()

    # Save the unique code
    UniqueCode.objects.create(code=code)


    return JsonResponse({
        "success": True,
        "code": code
    })




# =========================================
# SEARCH SERIAL API
# =========================================

@csrf_exempt
def search_serial_api(request):

    code = request.GET.get("serialno")

    serial = UniqueCode.objects.filter(code=code).values()

    if serial.exists():

        return JsonResponse({
            "success": True,
            "data": list(serial)
        })

    return JsonResponse({
        "success": False,
        "message": "Serial not found"
    }, status=404)


# =========================================
# SERIAL LIST API
# =========================================

@csrf_exempt
def serial_list_api(request):

    serials = UniqueCode.objects.all().values()

    return JsonResponse({
        "success": True,
        "data": list(serials)
    })


# =========================================
# UPDATE SERIAL API
# =========================================

@csrf_exempt
def update_serial_api(request):

    if request.method != "PUT":
        return JsonResponse({
            "success": False,
            "message": "PUT method required"
        }, status=405)

    try:

        data = json.loads(request.body)

        code = data.get("serialno")

        serial = UniqueCode.objects.get(code=code)

        serial.issuedto = data.get("issuedto")
        serial.subject = data.get("subject")
        serial.issuedate = data.get("issuedate")
        serial.issuername = data.get("issuername")

        serial.save()

        return JsonResponse({
            "success": True,
            "message": "Serial updated successfully"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)


# =========================================
# DONATION LIST API
# =========================================

def donation_list_api(request):

    donations = donation.objects.all().values()

    # TOTAL AMOUNT
    total_amount = donation.objects.aggregate(
        total=Sum('Amount')
    )['total'] or 0

    return JsonResponse({
        "success": True,
        "data": list(donations),
        "total_amount": total_amount
    })


# =========================================
# LOGIN HISTORY API
# =========================================
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


# =========================================
# HOME API
# =========================================

class HomeApi(View):

    def get(self, request):

        data = updates.objects.all().order_by('-id').values()

        return JsonResponse({
            "success": True,
            "updates": list(data)
        })


# Donation Qr Code API

@api_view(["POST"])
def donationdetail(request):

    try:

        # GET AMOUNT FROM REACT
        amount = request.data.get("amount")

        # VALIDATION
        if not amount:
            return Response(
                {
                    "success": False,
                    "message": "Amount is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # CREATE UPI LINK
        qr_text = (
            "upi://pay?"
            "pa=dhirajpatel08@okaxis"
            "&pn=DHIRAJ%20PATEL"
            f"&am={amount}"
            "&cu=INR"
            "&aid=uGICAgID1xJq5DA"
        )

        # GENERATE QR CODE
        qr_image = qrcode.make(qr_text, box_size=15)

        stream = BytesIO()

        qr_image.save(stream, format="PNG")

        qr_image_data = stream.getvalue()

        # CONVERT TO BASE64
        qr_image_base64 = base64.b64encode(
            qr_image_data
        ).decode("utf-8")

        # PHONEPE LINK
        upilinkPTM = (
            "https://mercury-uat.phonepe.com/transact/uat_v2?"
            "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        )

        # SEND RESPONSE TO REACT
        return Response(
            {
                "success": True,
                "amount": amount,
                "qr_image_base64": qr_image_base64,
                "upi_link": qr_text,
                "upilinkPTM": upilinkPTM
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


#Password rest email api views###


class PasswordResetAPIView(APIView):

    def post(self, request):

        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = (
                f"http://pjkss.com/"
                f"reset-password/{uid}/{token}/"
            )

            send_mail(
                'Password Reset',
                f'Click this link to reset password:\n{reset_link}',
                'yourgmail@gmail.com',
                [email],
                fail_silently=False,
            )

            return Response({
                'message': 'Password reset link sent successfully'
            })

        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)


class PasswordResetConfirmAPIView(APIView):

    def post(self, request):

        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)

            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()

                return Response({
                    'message': 'Password changed successfully'
                })

            return Response({
                'error': 'Invalid token'
            }, status=400)

        except Exception:
            return Response({
                'error': 'Something went wrong'
            }, status=400)

#Password rest manually api views###

class ChangePasswordAPIView(APIView):

    def post(self, request):

        email = request.data.get("email")
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        try:

            user = User.objects.get(email=email)

            # CHECK OLD PASSWORD
            if not user.check_password(old_password):

                return Response({
                    "success": False,
                    "message": "Old password is incorrect"
                })

            # CHANGE PASSWORD
            user.set_password(new_password)
            user.save()

            return Response({
                "success": True,
                "message": "Password changed successfully"
            })

        except User.DoesNotExist:

            return Response({
                "success": False,
                "message": "User not found"
            })






