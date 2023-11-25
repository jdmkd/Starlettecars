from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import uuid
from django.core.validators import FileExtensionValidator
import random
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django import template
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.mail import send_mail
# from .models import usertable, booking_table, vehicle_table, contactus, feedback
from .models import business_user, buss_vehicle, buss_contactus, buss_feedback
# from rentalapp.models import vehicle_table
def buss_index(request):
    try:
        if request.session["buss_log_id"]:
            id = request.session["buss_log_id"]
            userdata = request.session["buss_log_user"]
            buss_udata = business_user.objects.get(id=id)
            fetch_buss_vehicle = buss_vehicle.objects.filter(buss_vehicle_owner_id=id)
            print(fetch_buss_vehicle)
            buss_user_data = {
                    "userdata":userdata,
                    "buss_udata":buss_udata,
                    "fetch_buss_vehicle":fetch_buss_vehicle,
                }
    except KeyError as e:
        userdata = "Please login!!"
        buss_udata = "Please login!!"
        fetch_buss_vehicle = "Please login to fetch your vehicle details!!"
        buss_user_data = {
                    "userdata":userdata,
                    "buss_udata":buss_udata,
                    "fetch_buss_vehicle":fetch_buss_vehicle,
                }
        # print("this is exception: ",e)
        
    return render(request, "buss_index.html",buss_user_data)
    # return HttpResponse('Hello, welcome to the index page.')


def login_and_registration(request):
    try:
        if request.session["buss_log_id"]:
            print("already loggedIn")
            print("already loggedIn")

            return redirect("/rental_business")
    except Exception as e:
        print("exception you are not loggedIn::???", e)
        pass
    return render(request, "buss_accounts/login_and_registration.html")

# logout
def buss_logout(request):
    try:
        del request.session["buss_log_user"]
        del request.session["buss_log_id"]
        # print("Log out Successfuly....")
    except Exception as e:
        print("this is Exception :",e)
    return redirect("/rental_business")



def buss_login(request):
    try:
        if request.session["buss_log_id"]:
            print("already loggedIn")
            print("already loggedIn")

            return redirect("/rental_business")
    except Exception as e:
        print("exception you are not loggedIn::???", e)
        pass

    if request.method == "POST":
        try:
            buss_email = request.POST["buss_uemail"]
            buss_password = request.POST["buss_upass"]
            print("")
            if business_user.objects.filter(buss_emailid=buss_email).exists():
                buss_user_is = business_user.objects.filter(buss_emailid=buss_email).first()
                if buss_user_is.buss_is_verified:
                    try:
                        buss_user = business_user.objects.get(buss_emailid=buss_email, buss_password=buss_password)
                        request.session["buss_log_user"] = buss_user.buss_emailid
                        request.session["buss_log_id"] = buss_user.id
                        buss_user.update_buss_last_login()
                        request.session.save()
                        print("try user:::", buss_user)
                    except business_user.DoesNotExist:
                        buss_user = None
                        print("exception user is None:", buss_user)

                    if buss_user is not None:
                        # return render(request,'index.html')
                        print("User is Not None!!!")
                        return redirect("/rental_business")
                    else:
                        messages.error(request, "Password does not matched!!!")
                        print("Password does not matched!!!")
                else:
                    print("Please verify your account...")
                    messages.error(request, "Please verify your account...")

            else:
                messages.info(request, "account does not exist plz sign in")
                print("account does not exist plz sign in")
                return redirect('login_and_registration')
                # return render(request, "buss_accounts/login_and_registration.html")
        except Exception as e:
            print("this is main Exception ::", e)
    print("login bottom!!!!!!!!")
    return render(request, "buss_accounts/login_and_registration.html")


def buss_registeration(request):
    if request.method == "POST":
        buss_fname = request.POST["buss_fname"]
        buss_lname = request.POST["buss_lname"]
        buss_emailid = request.POST["buss_email"]
        buss_phone = request.POST["buss_phone_no"]
        buss_password = request.POST["buss_pass"]
        buss_rpassword = request.POST["buss_confm_pass"]
        # licence_no = request.POST["lnc_no"]
        # address = request.POST["ddress"]

        if (
            buss_emailid == ""
            or buss_fname == ""
            or buss_lname == ""
            or buss_phone ==""
            or buss_password == ""
            or buss_rpassword == ""
        ):
            messages.error(request, "Please Fill All Required Field.")

        elif buss_password == buss_rpassword:
            if business_user.objects.filter(buss_fname=buss_fname).exists():
                messages.info(
                    request, "Username Already Taken Please use Different username"
                )
                # return redirect('/')
            elif business_user.objects.filter(buss_emailid=buss_emailid).exists():
                messages.info(request, "With this Email user Already Exist")
                # return redirect('/')
            else:
                buss_auth_token = str(uuid.uuid4())
                registerdata = business_user(
                    buss_fname=buss_fname,
                    buss_lname=buss_lname,
                    buss_emailid=buss_emailid,
                    buss_phonenum=buss_phone,
                    buss_password=buss_password,
                    buss_rpassword=buss_rpassword,
                    buss_auth_token=buss_auth_token,
                    buss_role=2,
                    buss_status=1,
                )

                registerdata.save()
                print("buss user data saved...")
                buss_send_mail_after_registration(buss_emailid, buss_auth_token)
                print("Buss Account Registartion done go to gmail and verify ...")
                messages.success(request, "Buss Account Registartion done go to login page!")
                return redirect("mail_token_send")

        else:
            print("Your Password and Confirm Password does not Matched!!")
            messages.error(
                request, "Your Password and Confirm Password does not Matched!!"
            )
            # return redirect("/")
    else:
        print("last error occured!")
        # messages.error(request, "error occured!")

    print("last2 error occured!")
    print(str(uuid.uuid4()))
    # return render(request, "index.html")

    return render(request,"Buss_accounts/login_and_registration.html")

def buss_send_mail_after_registration(buss_emailid, buss_auth_token):
    try:
        subject = "Your Business Account needs to be varified."

        message = f"Hi paste the link to varify your account. http://127.0.0.1:8000/rental_business/email_verify/{buss_auth_token}"
        send_from = settings.EMAIL_HOST_USER
        print("This is send from gmail ::", send_from)
        recipient_list = [
            buss_emailid,
        ]
        print("this is recipient_list ::", recipient_list)
        send_mail(
            subject,
            message,
            send_from,
            recipient_list,
            fail_silently=False,
        )
        print("send_mail sended!!")
    except Exception as e:
        print("This is Exception..::", e)
        return False

    return True
    # return render("")


def email_verify(request, buss_auth_token):
    try:
        registerdata = business_user.objects.filter(buss_auth_token=buss_auth_token).first()
        print("verify...")
        if registerdata:
            if registerdata.buss_is_verified:
                messages.success(request, "Your account is already verified.")
                print("Your account is already verified.")

                return redirect("login_and_registration")
            
            registerdata.buss_is_verified = True
            registerdata.save()
            messages.success(request, "Your Business Account has been varified.")
            print("Your Business Account has been varified.")

            return redirect("login_and_registration")
        
        else:
            print("Else error")
            return redirect("verificationerror")
    except Exception as e:
        print(e)
    print("ends:::")
    # return True

def mail_token_send(request):
    return render(request, "buss_accounts/mail_token_sended.html")

def verificationerror(request):
    return render(request, "buss_accounts/verificationerror.html")

def generate_random_vehicle_id():
    if buss_vehicle.objects.exists():
        last_used_obj = buss_vehicle.objects.latest('buss_vehicle_id')
        last_used_id = str(last_used_obj.buss_vehicle_id)[3:]
        new_last_used_id = str(int(last_used_id) + 1)
        new_last_used_id = int(new_last_used_id)
    else:
        new_last_used_id = 1000

    new_vehicle_id = f'BUS{new_last_used_id:04d}'
    return new_vehicle_id
    
def add_new_vehicle(request):
    vehicle_company = buss_vehicle.VEHICLE_COMPANY_CHOICES
    vehicle_color = buss_vehicle.VEHICLE_COLOR_CHOICES
    vehicle_type = buss_vehicle.CAR_TYPE_CHOICES
    vehicle_status = buss_vehicle.VEHICLE_STATUS_CHOICES
    v_choice_data = {
        "vehicle_company":vehicle_company,
        "vehicle_color":vehicle_color,
        "vehicle_type":vehicle_type,
        "vehicle_status":vehicle_status,
        }
    if request.method == "POST" and request.FILES.get("buss_vehicle_photo"):
        buss_vehicle_photo = request.FILES["buss_vehicle_photo"]
        new_vehicle_id = generate_random_vehicle_id()
        bid = request.session["buss_log_id"]
        buss_vehicle_company_name = request.POST["buss_vehicle_company_name"]
        buss_vehicle_model_name = request.POST["buss_vehicle_model_name"]
        buss_vehicle_type = request.POST["buss_vehicle_type"]
        buss_vehicle_color = request.POST["buss_vehicle_color"]
        buss_vehicle_number = request.POST["buss_vehicle_number"]
        buss_vehicle_location = request.POST["buss_vehicle_location"]
        buss_rent_per_day = request.POST["buss_rent_per_day"]
        buss_vehicle_status = request.POST["buss_vehicle_status"]
        buss_vehicle_description = request.POST["buss_vehicle_description"]

        buss_data = buss_vehicle(
                buss_vehicle_id = new_vehicle_id,
                buss_vehicle_owner = business_user(id=bid),
                buss_vehicle_company_name = buss_vehicle_company_name,
                buss_vehicle_model = buss_vehicle_model_name,
                buss_vehicle_color = buss_vehicle_color,
                buss_vehicle_type = buss_vehicle_type,
                buss_vehicle_number = buss_vehicle_number,
                buss_vehicle_location = buss_vehicle_location,
                buss_rent_per_day = buss_rent_per_day,
                buss_vehicle_photo = buss_vehicle_photo,
                buss_vehicle_description = buss_vehicle_description,
                buss_vehicle_status = buss_vehicle_status,
            )
        buss_data.save()
        messages.success(request,f"New vehicle '{ buss_data } - {buss_data.buss_vehicle_model}' has been added successfuly, Now user can book your '{buss_data}-{buss_data.buss_vehicle_model}' on rent.")
        return redirect("add_new_vehicle")
        
    else:
        print("this is else!!")
    return render(request,"add_new_vehicle.html",{"v_choice_data":v_choice_data})




def buss_profile(request): 
    return render(request,"Buss_profile/myprofile.html")