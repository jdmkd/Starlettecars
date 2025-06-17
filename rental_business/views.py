from datetime import datetime, timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import uuid
from decouple import config
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
import json
from django.db.models import Count, Sum, F, FloatField
from django.db.models.functions import Cast
from django.db.models.functions import Lower, Trim, ExtractMonth, ExtractYear

from django.core.serializers.json import DjangoJSONEncoder

from rentalapp.models import booking_table, usertable
# from .models import usertable, booking_table, vehicle_table, contactus, feedback
from .models import business_user, buss_vehicle, buss_contactus, buss_feedback
# from rentalapp.models import vehicle_table



def dashboard(request):
    try:
        if request.session["buss_log_id"]:
            id = request.session["buss_log_id"]
            userdata = request.session["buss_log_user"]
            buss_udata = business_user.objects.get(id=id)

            # All vehicles owned by this business
            fetch_buss_vehicle = buss_vehicle.objects.filter(buss_vehicle_owner_id=id)
            
            # All bookings for this user's vehicles
            fetch_booked_vdata = booking_table.objects.filter(
                vehicle_id__in=fetch_buss_vehicle
            ).order_by('-booking_date')

            # Booking status counts
            approved_count = fetch_booked_vdata.filter(status='approved').count()
            rejected_count = fetch_booked_vdata.filter(status='rejected').count()
            pending_count = fetch_booked_vdata.filter(status='pending').count()
            canceled_count = fetch_booked_vdata.filter(is_cancelled=True).count()
            total_booking_count = fetch_booked_vdata.count()
            registered_vehicles_count = fetch_buss_vehicle.count()
            
            # Calculate total revenue for approved bookings
            total_revenue = 0
            approved_bookings = fetch_booked_vdata.filter(status='approved')
            for booking in approved_bookings:
                try:
                    total_revenue += float(booking.amount)
                except ValueError:
                    print(f"Invalid amount for booking ID {booking.id}")
            
            total_revenue = round(total_revenue, 2)
            
            # Calculate total revenue for approved bookings by month
            revenue_by_month = fetch_booked_vdata.filter(status='approved') \
                .annotate(
                    amount_float=Cast('amount', output_field=FloatField()),
                    month=ExtractMonth('booking_date'),
                    year=ExtractYear('booking_date')
                ) \
                .values('year', 'month') \
                .annotate(total=Sum('amount_float')) \
                .order_by('year', 'month')


            month_labels = []
            month_revenue = []

            month_map = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            for entry in revenue_by_month:
                month_num = entry['month']
                year = entry['year']
                month_labels.append(f"{month_map[month_num - 1]} {year}")
                month_revenue.append(round(float(entry['total']), 2))


            # Vehicle types pie chart
            vehicle_type_counts = fetch_buss_vehicle.values('buss_vehicle_type').annotate(count=Count('id'))
            type_labels = []
            type_counts = []
            for entry in vehicle_type_counts:
                type_labels.append(entry['buss_vehicle_type'])
                type_counts.append(entry['count'])

            # Top vehicles by booking count
            top_vehicles = fetch_booked_vdata.values(
                'vehicle_id__buss_vehicle_company_name', 'vehicle_id__buss_vehicle_model'
            ).annotate(count=Count('id')).order_by('-count')[:5]

            top_vehicle_labels = []
            top_vehicle_counts = []
            for item in top_vehicles:
                label = f"{item['vehicle_id__buss_vehicle_company_name']} {item['vehicle_id__buss_vehicle_model']}"
                top_vehicle_labels.append(label)
                top_vehicle_counts.append(item['count'])

            # Payment method distribution (if available)
            # fetch_booked_vdata.filter(paystatus='paid')
            payment_distribution = (
                fetch_booked_vdata
                .annotate(payment_clean=Trim(Lower('payment_method')))
                .values('payment_clean')
                .annotate(count=Count('id'))
                .order_by('-count')
            )
            
            payment_labels = []
            payment_counts = []

            for entry in payment_distribution:
                label = entry['payment_clean'].capitalize()  # Optional: 'cash' -> 'Cash'
                count = entry['count']

                payment_labels.append(label)
                payment_counts.append(count)

            # Add monthly booking count for bar/mixed chart
            bookings_by_month = fetch_booked_vdata.values('booking_date__month').annotate(count=Count('id')).order_by('booking_date__month')

            booking_month_labels = []
            booking_month_counts = []

            for entry in bookings_by_month:
                month_num = entry['booking_date__month']
                booking_month_labels.append(month_map[month_num - 1])
                booking_month_counts.append(entry['count'])

            
                
            # Prepare data for the template
            buss_user_data = {
                "userdata": userdata,
                "buss_udata": buss_udata,
                "fetch_booked_vdata": fetch_booked_vdata,
                "fetch_buss_vehicle":fetch_buss_vehicle,
                "approved_count": approved_count,
                "rejected_count": rejected_count,
                "pending_count": pending_count,
                "canceled_count": canceled_count,
                "total_booking_count": total_booking_count,
                "registered_vehicles_count": registered_vehicles_count,
                "total_revenue": total_revenue,

                # Chart datasets
                "month_labels": json.dumps(month_labels),
                "month_revenue": json.dumps(month_revenue),
                "type_labels": json.dumps(type_labels),
                "type_counts": json.dumps(type_counts),
                "top_vehicle_labels": json.dumps(top_vehicle_labels),
                "top_vehicle_counts": json.dumps(top_vehicle_counts),
                "payment_labels": json.dumps(payment_labels),
                "payment_counts": json.dumps(payment_counts),
                "booking_month_labels": json.dumps(booking_month_labels),
                "booking_month_counts": json.dumps(booking_month_counts),
                
            }

            return render(request, "dashboard/dashboard.html", buss_user_data)
    except KeyError as e:
        print("business user is not logged in")
        pass

    
    # if not month_labels or not month_revenue:
    month_labels = ['Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024']
    month_revenue = [1200, 1500, 900, 1800]

    # if not booking_month_labels or not booking_month_counts:
    booking_month_labels = ['Jan', 'Feb', 'Mar', 'Apr']
    booking_month_counts = [3, 5, 2, 4]

    # Fallbacks for empty vehicle types
    # if not type_labels or not type_counts:
    type_labels = ['SUV', 'Sedan', 'Hatchback']
    type_counts = [5, 3, 2]

    # Fallbacks for top vehicles
    # if not top_vehicle_labels or not top_vehicle_counts:
    top_vehicle_labels = ['Toyota Fortuner', 'Hyundai Creta', 'Maruti Swift']
    top_vehicle_counts = [10, 7, 4]

    # Fallbacks for payment method distribution
    # if not payment_labels or not payment_counts:
    payment_labels = ['Cash', 'Card', 'UPI']
    payment_counts = [8, 5, 7]

    buss_user_data = {
        # Chart datasets
        "month_labels": json.dumps(month_labels),
        "month_revenue": json.dumps(month_revenue),
        "type_labels": json.dumps(type_labels),
        "type_counts": json.dumps(type_counts),
        "top_vehicle_labels": json.dumps(top_vehicle_labels),
        "top_vehicle_counts": json.dumps(top_vehicle_counts),
        "payment_labels": json.dumps(payment_labels),
        "payment_counts": json.dumps(payment_counts),
        "booking_month_labels": json.dumps(booking_month_labels),
        "booking_month_counts": json.dumps(booking_month_counts),
    }

    return render(request, "dashboard/dashboard.html", buss_user_data)




def registered_vehicles(request):
    try:
        if request.session["buss_log_id"]:
            id = request.session["buss_log_id"]
            userdata = request.session["buss_log_user"]
            buss_udata = business_user.objects.get(id=id)
            fetch_buss_vehicle = buss_vehicle.objects.filter(buss_vehicle_owner_id=id)
            # print(fetch_buss_vehicle)
            buss_user_data = {
                    "userdata":userdata,
                    "buss_udata":buss_udata,
                    "fetch_buss_vehicle":fetch_buss_vehicle,
                }
            return render(request, "registered_vehicles.html",buss_user_data)
    except KeyError as e:
        pass
        # print("this is exception: ",e)
    
    return redirect("/rental_business")
    # return HttpResponse('Hello, welcome to the index page.')


def registered_vehicle_details(request):
    try:
        if request.session["buss_log_id"] or request.method == "POST":
            print("OK!!")
            vehicle_id=request.POST["vehicle_id"]

            id = request.session["buss_log_id"]
            userdata = request.session["buss_log_user"]

            buss_udata = business_user.objects.get(id=id)
            
            fetch_buss_vehicle = buss_vehicle.objects.filter(buss_vehicle_owner_id=id)
            vehicle_details_queryset = buss_vehicle.objects.get(id=vehicle_id)

            buss_vehicle_details = {
                    "userdata":userdata,
                    "buss_udata":buss_udata,
                    "vehicle_details_list":vehicle_details_queryset,
                }
            return render(request, "registered_vehicle_details.html",buss_vehicle_details)
    except KeyError as e:
        print("Exception",e)
        pass
        # print("this is exception: ",e)
        
    return redirect("/rental_business")
    



def registered_vehicle_detailsx(request):
    try:
        if request.session.get("buss_log_id") and request.method == "POST":
            print("OK!!")

            # Retrieve the business user data from the session
            id = request.session["buss_log_id"]
            userdata = request.session["buss_log_user"]
            buss_udata = business_user.objects.get(id=id)

            # Initialize variables for vehicle details
            vehicle_details_queryset = None
            booked_vehicle_id = None
            vehicle_id = None

            # Handle different POST requests
            try:
                if "booked_vehicle_id" in request.POST:
                    booked_vehicle_id = request.POST["booked_vehicle_id"]
                    vehicle_details_queryset = buss_vehicle.objects.filter(id=booked_vehicle_id)
                    print("this is booked_vehicle_id:",booked_vehicle_id)
                if "vehicle_id" in request.POST:
                    vehicle_id = request.POST["vehicle_id"]
                    vehicle_details_queryset = buss_vehicle.objects.filter(id=vehicle_id)
                    print("this is vehicle_id:",vehicle_id)
            except Exception as e:
                print("Error in processing vehicle details:", e)
                vehicle_details_queryset = []

            # If no specific vehicle data is found, default to all vehicles owned by the business
            if not vehicle_details_queryset:
                vehicle_details_queryset = buss_vehicle.objects.filter(buss_vehicle_owner_id=id)
                print("not vehicle_details_queryset ::",vehicle_details_queryset)
            # Prepare data to be passed to the template
            buss_vehicle_details = {
                "userdata": userdata,
                "buss_udata": buss_udata,
                "vehicle_details_list": vehicle_details_queryset,
            }

            return render(request, "registered_vehicle_details.html", buss_vehicle_details)

    except KeyError as e:
        print("Session KeyError:", e)
        pass

    except Exception as e:
        print("Exception:", e)

    return redirect("/rental_business")



# registered_vehicle_details_update.html
def registered_vehicle_details_update(request):
    try:
        if request.session["buss_log_id"]:
            id = request.session["buss_log_id"]
            userdata = request.session["buss_log_user"]
            # print("OK!!!!!!!!!!!!!")
            if request.method == "POST":
                try:
                    vehicle_id=request.POST["vehicle_id"]
                    buss_udata = business_user.objects.get(id=id)
                    vehicle_details_queryset = buss_vehicle.objects.get(id=vehicle_id)

                    buss_vehicle_details = {
                            "vehicle_details_list":vehicle_details_queryset,
                            "buss_udata":buss_udata
                        }
                    return render(request, "registered_vehicle_details_update.html",buss_vehicle_details)
                except:
                    pass
            

            
            # return render(request, "registered_vehicle_details_update.html",buss_vehicle_details)
    except KeyError as e:
        pass
        
    return redirect("/rental_business")


def registered_vehicle_details_update_done(request):
    try:
        if request.session["buss_log_id"]:
            id = request.session["buss_log_id"]
            userdata = request.session["buss_log_user"]
            # print("OK!!!!!!!!!!!!!")
            if request.method == "POST":
                vehicle_id=request.POST["vehicle_id"]
                vehicle_details_queryset = buss_vehicle.objects.get(id=vehicle_id)
                

                buss_vehicle_company_name=request.POST["buss_vehicle_company_name"]
                buss_vehicle_model=request.POST["buss_vehicle_model"]
                buss_vehicle_color=request.POST["buss_vehicle_color"]
                buss_vehicle_type=request.POST["buss_vehicle_type"]
                buss_vehicle_location=request.POST["buss_vehicle_location"]
                buss_rent_per_day=request.POST["buss_rent_per_day"]
                buss_vehicle_description=request.POST["buss_vehicle_description"]
                


                buss_chassi_number = request.POST["buss_chassi_number"]
                print("buss_chassi_number :" ,buss_chassi_number)
                if vehicle_details_queryset.buss_chassi_number:
                    print("vehicle_details_queryset.buss_chassi_number ::", vehicle_details_queryset.buss_chassi_number)
                # if buss_vehicle.objects.filter(buss_chassi_number=buss_chassi_number).exists():
                #     print("This chassis number already exists.")
                #     messages.error(request,'This chassis number already exists.')
                #     return render(request, "registered_vehicle_details_update.html",{"vehicle_details_list":vehicle_details_queryset,})
                    
                    

                    # Booking status counts
                    # approved_count = fetch_booked_vdata.filter(status='approved').count()

                print("After buss_chassi_number!!")
                buss_year_of_manufacture = request.POST["buss_year_of_manufacture"]
                buss_registration_date = request.POST["buss_registration_date"]
                print("")

                buss_vehicle_location = request.POST["buss_vehicle_location"]
                buss_rent_per_day = request.POST["buss_rent_per_day"]
                buss_vehicle_status = request.POST["buss_vehicle_status"]
                buss_vehicle_description = request.POST["buss_vehicle_description"]


                # buss_vehicle_is_soldout=request.POST["buss_vehicle_is_soldout"]
                # buss_vehicle_status=request.POST["buss_vehicle_status"]
                # buss_vehicle_photo

                print("buss_vehicle_company_name :",buss_vehicle_company_name)
                print("buss_rent_per_day ::",buss_rent_per_day)
                

                vehicle_details_queryset.buss_vehicle_company_name = buss_vehicle_company_name
                vehicle_details_queryset.buss_vehicle_model=buss_vehicle_model
                vehicle_details_queryset.buss_vehicle_color=buss_vehicle_color
                print("V validation!!")
                vehicle_details_queryset.buss_chassi_number=buss_chassi_number
                vehicle_details_queryset.buss_year_of_manufacture=buss_year_of_manufacture
                vehicle_details_queryset.buss_registration_date=buss_registration_date
                print("after V validation!!")

                vehicle_details_queryset.buss_vehicle_status=buss_vehicle_status
                print("buss_vehicle_status ",buss_vehicle_status)

                vehicle_details_queryset.buss_vehicle_type=buss_vehicle_type
                vehicle_details_queryset.buss_vehicle_location=buss_vehicle_location
                vehicle_details_queryset.buss_rent_per_day=buss_rent_per_day
                vehicle_details_queryset.buss_vehicle_description=buss_vehicle_description

                vehicle_details_queryset.save()
                print("you vehicle have been updated Successfully!!")
                messages.success(request,"vehicle have been updated Successfully!!")


                buss_vehicle_details = {
                            "vehicle_details_list":vehicle_details_queryset,
                        }
                return render(request, "registered_vehicle_details_update.html",buss_vehicle_details)
            
        else:
            return redirect("/rental_business")

    except Exception as e:
        print("Exception :",e)
        pass
    # return render(request, "registered_vehicle_details_update.html")
    return redirect("/rental_business")


def login_and_registration(request):
    try:
        if request.session["buss_log_id"]:
            # print("already loggedIn")

            return redirect("/rental_business")
    except Exception as e:
        # print("exception you are not loggedIn::???", e)
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

            return redirect("/rental_business")
    except Exception as e:
        print("exception you are not loggedIn::???", e)
        pass

    if request.method == "POST":
        try:
            buss_email = request.POST["buss_uemail"]
            buss_password = request.POST["buss_upass"]
            # print("")
            if business_user.objects.filter(buss_emailid=buss_email).exists():
                buss_user_is = business_user.objects.filter(buss_emailid=buss_email).first()
                if buss_user_is.buss_is_verified:
                    try:
                        buss_user = business_user.objects.get(buss_emailid=buss_email, buss_password=buss_password)
                        request.session["buss_log_user"] = buss_user.buss_emailid
                        request.session["buss_log_id"] = buss_user.id
                        buss_user.update_buss_last_login()
                        request.session.save()
                        # print("try user:::", buss_user)
                    except business_user.DoesNotExist:
                        buss_user = None
                        # print("exception user is None:", buss_user)

                    if buss_user is not None:
                        # return render(request,'index.html')
                        # print("User is Not None!!!")
                        messages.success(request, "Buss Account Login successful!", extra_tags="login_success")
                        return redirect("/rental_business")
                    else:
                        messages.error(request, "Password does not matched!!!")
                        # print("Password does not matched!!!")
                else:
                    # print("Please verify your account...")
                    messages.error(request, "Please verify your account...")

            else:
                messages.info(request, "account does not exist plz sign in")
                print("account does not exist plz sign in")
                return redirect('login_and_registration')
                # return render(request, "buss_accounts/login_and_registration.html")
        except Exception as e:
            print("this is main Exception ::", e)
            pass
    # print("login bottom!!!!!!!!")
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
                messages.success(request, "Buss Account Registration successful!", extra_tags="registration_success")
                return redirect("login_and_registration")
                
                # return render(request,"buss_accounts/login_and_registration.html")

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

    return render(request,"buss_accounts/login_and_registration.html")

def buss_send_mail_after_registration(buss_emailid, buss_auth_token):
    try:
        subject = "Your Business Account needs to be varified."

        message = f"Hi paste the link to varify your account. {config('END_POINT_URL')}/rental_business/email_verify/{buss_auth_token}"
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
    
def add_vehicle(request):
    try:
        if request.session["buss_log_id"]:
            id = request.session["buss_log_id"]
            
            buss_udata = business_user.objects.get(id=id)

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

                buss_chassi_number = request.POST["buss_chassi_number"]
                print("buss_chassi_number :" ,buss_chassi_number)
                if buss_vehicle.objects.filter(buss_chassi_number=buss_chassi_number).exists():
                    print("This chassis number already exists.")
                    messages.error(request,'This chassis number already exists.')
                print("After buss_chassi_number!!")
                buss_year_of_manufacture = request.POST["buss_year_of_manufacture"]
                buss_registration_date = request.POST["buss_registration_date"]
                print("")

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

                        buss_chassi_number = buss_chassi_number,
                        
                        buss_year_of_manufacture = buss_year_of_manufacture,
                        buss_registration_date = buss_registration_date,

                        buss_vehicle_location = buss_vehicle_location,
                        buss_rent_per_day = buss_rent_per_day,
                        buss_vehicle_photo = buss_vehicle_photo,
                        buss_vehicle_description = buss_vehicle_description,
                        buss_vehicle_status = buss_vehicle_status,
                    )
                buss_data.save()
                messages.success(request,f"New vehicle '{ buss_data } - {buss_data.buss_vehicle_model}' has been added successfuly, Now user can book your '{buss_data}-{buss_data.buss_vehicle_model}' on rent.")
                
            return render(request,"add_vehicle.html",{"v_choice_data":v_choice_data,"buss_udata":buss_udata})
                
        else:
            return redirect("/rental_business")
            # return redirect("/rental_business")
    except Exception as e:
        print("Exception :",e)

        # return redirect("/rental_business")
    return redirect("/rental_business")
    # return render(request,"add_vehicle.html",{"v_choice_data":v_choice_data,"buss_udata":buss_udata})




def vehicle_booking_approval(request):
    try:
        if request.session["buss_log_id"]:
            id = request.session["buss_log_id"]
            buss_udata = business_user.objects.get(id=id)
            if request.method == "POST":
                action = request.POST.get("action")
                booked_vehicle_id = request.POST.get("booked_vehicle_id")

                try:
                    
                    booked_vehicle = booking_table.objects.get(id=booked_vehicle_id)

                    if action == "approve":
                        booked_vehicle.status = "approved"
                        booked_vehicle.vehicle_id.buss_vehicle_status = 'Booked'
                        booked_vehicle.vehicle_id.save()
                        message = f"Vehicle ID {booked_vehicle_id} has been approved."

                    elif action == "reject":
                        booked_vehicle.status = "rejected"
                        booked_vehicle.vehicle_id.buss_vehicle_status="Available"
                        booked_vehicle.vehicle_id.save()
                        message = f"Vehicle ID {booked_vehicle_id} has been rejected."

                    else:
                        print(f"Wrong request :: action={action} and id={booked_vehicle_id}")
                    # booked_vehicle.approval_date = timezone.now()
                    booked_vehicle.save()


                except booking_table.DoesNotExist:
                    return HttpResponse("Booked vehicle not found.", status=404)
            
            
            fetch_booked_vdata = booking_table.objects.filter(
                vehicle_id__in=buss_vehicle.objects.filter(buss_vehicle_owner_id=id)
            ).order_by('-booking_date')
            
            fetch_booked_vdata = {
                    "buss_udata":buss_udata,
                    "fetch_booked_vdata":fetch_booked_vdata,
            }
            return render(request,"vehicle_booking_approval.html", fetch_booked_vdata )
        
    except Exception as e:
        print("Exception xx : ",e)
        pass

    # return render(request,"vehicle_booking_approval.html")
    return redirect("/rental_business")

def view_user_detail_for_approval(request):
    try:
        if request.session["buss_log_id"]:
            id = request.session["buss_log_id"]
            if request.method == "POST":
                booked_vehicle_uid = request.POST.get("booked_vehicle_uid")
                

                try:
                    # Fetch the booked vehicle object from the database
                    booking_req_by_user = usertable.objects.get(id=booked_vehicle_uid)
                except booking_table.DoesNotExist:
                    return HttpResponse("user detail not found.", status=404)
            
            
            # fetch_booked_vdata = booking_table.objects.filter(
            #     vehicle_id__in=buss_vehicle.objects.filter(buss_vehicle_owner_id=id)
            # ).order_by('-booking_date')
            
            booking_req_by_user = {
                    # "buss_udata":buss_udata,
                    "booking_req_by_user":booking_req_by_user,
            }
            return render(request,"view_user_detail_for_approval.html", booking_req_by_user)
        
    except Exception as e:
        return redirect("/rental_business/vehicle/booking/approval")
        

    # return render(request,"vehicle_booking_approval.html")
    return redirect("/rental_business")



def buss_profile(request):
    try:
        print("buss_profile trying")
        if request.session["buss_log_id"]:
            b_log_user = request.session["buss_log_user"]
            b_log_id = request.session["buss_log_id"]
            # buss_udata = business_user.objects.get(id=id)
            business_udata = business_user.objects.filter(id=b_log_id)[0]
        return render(request,"buss_profile/myprofile.html", {"business_udata": business_udata,"buss_udata":business_udata})
    
    
    except Exception as e:
        userdata = "Please login!!"
        print(userdata)
        print("Exceptionx : ",e)
        pass
    print("redirecting to the /rental_business")
    return redirect("/rental_business")


def buss_profile_edit(request):
    try:
        if request.session["buss_log_id"]:
            b_log_user = request.session["buss_log_user"]
            b_log_id = request.session["buss_log_id"]
            
            if request.method == "POST":
                # user_profile_image_upload = request.POST.get("user_profile_image_upload")
                bus_firstname = request.POST.get("bus_firstname")
                bus_lastname = request.POST.get("bus_lastname")
                bus_phonenum = request.POST.get("bus_phonenum")


                buss_date_of_birth = request.POST.get("buss_date_of_birth")
                buss_aadhaar_number = request.POST.get("buss_aadhaar_number")
                buss_driver_license_number = request.POST.get("buss_driver_license_number")
                buss_driver_license_expiry = request.POST.get("buss_driver_license_expiry")
                buss_address_line1 = request.POST.get("buss_address_line1")
                buss_address_line2 = request.POST.get("buss_address_line2")
                buss_city = request.POST.get("buss_city")
                buss_state = request.POST.get("buss_state")
                buss_zip_code = request.POST.get("buss_zip_code")
                buss_country = request.POST.get("buss_country")

                


                try:
                    buss_user = business_user.objects.get(id=b_log_id)
                    buss_user.buss_fname = bus_firstname
                    buss_user.buss_lname = bus_lastname
                    buss_user.buss_phonenum = bus_phonenum
                    
                    buss_user.buss_date_of_birth = buss_date_of_birth
                    buss_user.buss_aadhaar_number = buss_aadhaar_number
                    buss_user.buss_driver_license_number = buss_driver_license_number
                    buss_user.buss_driver_license_expiry = buss_driver_license_expiry
                    buss_user.buss_address_line1 = buss_address_line1
                    buss_user.buss_address_line2 = buss_address_line2
                    buss_user.buss_city = buss_city
                    buss_user.buss_state = buss_state
                    buss_user.buss_zip_code = buss_zip_code
                    buss_user.buss_country = buss_country
                    


                    buss_user.save()

                    print("You profile updated!")

                    try:
                        if request.method == "POST" and request.FILES.get("bus_user_profile_image_upload"):
                            buss_updProfile_photo = request.FILES["bus_user_profile_image_upload"]
                            
                            # userdata = usertable.objects.filter(id=logid)[0]
                            if buss_updProfile_photo:
                                # print("buss_updProfile_photo:::",buss_updProfile_photo)
                                valid_extensions = ["jpg", "jpeg", "png", "gif","webp"]
                                validator = FileExtensionValidator(
                                    allowed_extensions=valid_extensions,
                                    message="Please upload a valid image file.",
                                )
                                try:
                                    validator(buss_updProfile_photo)


                                except ValidationError as e:
                                    messages.error(request,"Please upload a valid image file.")
                                    return redirect("editprofile")
                                buss_user.buss_updProfile_photo = buss_updProfile_photo
                                buss_user.save()
                                # return render(request,"Userprofile/editprofile/editprofile.html",context)
                                return redirect("buss_profile")
                    except Exception as e:
                        print("Exception ::",e)
                        pass
                    messages.success(request, "Your profile has been updated.")
                    return redirect("buss_profile")
                    # buss_profile
                except business_user.DoesNotExist:
                    return HttpResponse("user detail not found.", status=404)

            business_udata = business_user.objects.filter(id=b_log_id)[0]
        return render(request,"buss_profile/editprofile.html", {"business_udata": business_udata, "buss_udata":business_udata})
    
    
    except Exception as e:
        print("Exception ::",e)
        userdata = "Please login!!"
        print(userdata)
        pass
    return redirect("/rental_business")