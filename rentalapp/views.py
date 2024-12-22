from datetime import datetime
from django.utils import timezone
from datetime import timedelta
import os
import email
import uuid
import random
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.conf import settings
from .models import usertable, booking_table, contactus, feedback
from rental_business.models import buss_vehicle
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.utils.dateparse import parse_datetime




def index(request):
    try:
        if request.session["log_id"]:
            id = request.session["log_id"]
            userdata = request.session["log_user"]
            udata = usertable.objects.filter(id=id)[0]
    except KeyError:
        userdata = "Please login!!"
        udata = "Please login!!"

    fetchvehicle = buss_vehicle.objects.all()
    vlist = list(fetchvehicle)
    if fetchvehicle:
        for i in range(1, len(fetchvehicle) + 1):
            if i <= len(vlist):
                x = random.sample(vlist, i)
    else:
        x = None

    return render(request,"index.html",{"vehicle": fetchvehicle, "x": x, "udata": udata, "userdata": userdata})


def termsandconpage(request):
    return render(request, "termsandconpage.html")

def services(request):
    try:
        if request.session["log_id"]:
            id = request.session["log_id"]
            udata = usertable.objects.filter(id=id)[0]
    except KeyError:
        udata = "Please login!!"
    return render(request, "services.html", {"udata": udata})


# def loginform(request):
#     return render(request,'loginform.html')
#
# def loginform2(request):
#     return render(request,'loginform2.html')


def vehicles(request):
    try:
        if request.session["log_id"]:
            id = request.session["log_id"]
            userdata = request.session["log_user"]
            udata = usertable.objects.filter(id=id)[0]
    except KeyError:
        userdata = "Please login!!"
        udata = "Please login!!"
    fetchvehicle = buss_vehicle.objects.all()
    vlist = list(fetchvehicle)
    
    if fetchvehicle:
        for i in range(1, len(fetchvehicle) + 1):
            if i <= len(vlist):
                x = random.sample(vlist, i)
    else:
        x = None
    # x = list(buss_vehicle.objects.all())
    # x = random.sample(x, 9)
    return render(request, "vehicles.html", {"vehicle": fetchvehicle, "x": x, "udata": udata})


def contact(request):
    try:
        if request.session["log_id"]:
            id = request.session["log_id"]
            userdata = request.session["log_user"]
            udata = usertable.objects.filter(id=id)[0]
    except KeyError:
        userdata = "Please login!!"
        udata = "Please login!!"
    return render(request, "contact.html", {"udata": udata})


def feedbackpage(request):
    try:
        if request.session["log_id"]:
            id = request.session["log_id"]
            userdata = request.session["log_user"]
            udata = usertable.objects.filter(id=id)[0]
    except KeyError:
        userdata = "Please login!!"
        udata = "Please login!!"
    return render(request, "feedback.html", {"udata": udata})


def feedbackshow(request):
    try:
        if request.method == "POST":
            if request.session["log_id"]:
                uid = request.session["log_id"]
                print("uid =",uid)
                name = request.POST.get("name")
                email = request.POST.get("email")
                comment = request.POST.get("comments")
                ratings = request.POST.get("rating1")
                feedbackdata = feedback(
                    name=name,email=email, comments=comment, l_id=usertable(id=uid), ratings=ratings
                )  # l_id=usertable(id=uid)
                feedbackdata.save()
                messages.success(request, "feedback has been submitted!")
                return redirect("/feedback")
            else:
                messages.success(request, "please login..")
                return redirect("login")
        # else:
        #     print("request.method is not POST")
    except Exception as e:
        print("exception is :",e)
        messages.error(request, f"all fields are required.")


    return redirect("/feedback")


# @login_required
def checkout(request, id):
    try:
        if request.session["log_id"]:
            uid = request.session["log_id"]
            userdata = request.session["log_user"]
            udata = usertable.objects.filter(id=uid)[0]
    except KeyError:
        userdata = "Please login!!"
        udata = "Please login!!"
    fetch = buss_vehicle.objects.get(id=id)
    return render(request, "checkout.html", {"vehicle": fetch, "udata":udata})

def checkoutform(request):
    return render(request, "checkoutform.html")

def vehicle_booking(request):
    # print("inside the vehicle booking")
    if request.method == "POST":
        try:
            if request.session["log_id"]:
                from_duration = request.POST.get("sdate")
                to_duration = request.POST.get("edate")
                uid = request.session["log_id"]
                vid = request.POST.get("vid")
                rupee = request.POST.get("rupee")
                
                service_charges = 250.0
                tax_percentage = 18
                


                date_format = "%Y-%m-%d"
                from_date = datetime.strptime(str(from_duration), date_format)
                to_date = datetime.strptime(str(to_duration), date_format)
                today = datetime.today().date()
                current_date =datetime.strptime(str(today), date_format)
                
                if usertable.objects.get(id=uid):
                    user=usertable.objects.get(id=uid)
                    if user.aadhaar_number and user.validate_aadhaar() and user.date_of_birth and user.driver_license_number and user.driver_license_expiry and user.is_license_valid() and user.validate_license():
                        print("==>>>>>>>>>>")
                        if from_date < current_date:
                            messages.error(request, "From date cannot be in the past!")
                            return redirect("checkout/{}".format(vid))
                        if to_date < current_date:
                            messages.error(request, "To date cannot be in the past.")
                            return redirect("checkout/{}".format(vid))
                        if from_date > to_date:
                            messages.error(request, "Please Enter a Valid Date Format!")
                            return redirect("checkout/{}".format(vid))
                        # if today(a) and today(to_date):
                        #     print("today.................")
                        

                        if to_date > from_date:
                            delta = to_date - from_date
                            dayss = int(delta.days)
                            
                            amount = dayss * int(rupee)
                            base_rental = float(amount)  # Assuming `amount` is a field in the model
                            tax_amount = base_rental * tax_percentage / 100
                            total_rental_amount = base_rental + service_charges + tax_amount
                            
                            vehicle_status = buss_vehicle.objects.get(id=vid)
                            
                            if vehicle_status.buss_chassi_number is None:
                                messages.error(request, "This Vehicle is not approved!!")
                            if vehicle_status.buss_vehicle_status == "Booked":
                                messages.success(request, "This Vehicle is Already Booked!")
                                # print("redirected same vehicle page....")
                            if vehicle_status.buss_vehicle_status == "Under Maintenance":
                                messages.success(request, "This Vehicle is in Under Maintenance!")
                                # print("redirected same vehicle page....")
                            if vehicle_status.buss_vehicle_status == "Out of Service":
                                messages.success(request, "This Vehicle is Out of Service!")
                                # print("redirected same vehicle page....")


                            if vehicle_status.buss_vehicle_status == "Available" and vehicle_status.buss_chassi_number is not None:
                                vehicle_status.buss_vehicle_status = "Booked"
                                vehicle_status.save()

                                bookingdata = booking_table(
                                    amount=total_rental_amount,
                                    from_to=to_duration,
                                    from_duration=from_duration,
                                    login_id=usertable(id=uid),
                                    vehicle_id=buss_vehicle(id=vid), #, buss_vehicle_status=vehicle_status
                                    paystatus=1,
                                )
                                bookingdata.save()
                                messages.success(request, "Booking Done!")
                                # print("redirected to booking history page....")
                                return redirect("/booking/history")
                        else:
                            # fetch = buss_vehicle.objects.get(vid=vid)
                            messages.error(request, "Please Enter a Valid Date Formate!!!")
                    else:
                        messages.error(request, "please update you profile to validate you authenticity!!")
                        return redirect("editprofile")
            # else:
                # print("session log_id are not available!!")
        except KeyError:
            # print("please login to continue.....")
            messages.error(request,"please login...")
            pass
    else:
        messages.error(request, "error occured!")
        # print("error occured!")

    vid = request.POST.get("vid")
    return redirect("checkout/{}".format(vid))


# @login_required()
def booking_history(request):
    try:
        if request.session["log_id"]:
            uid = request.session["log_id"]

            vdata = booking_table.objects.filter(login_id=uid).order_by('-booking_date')
            
            if request.method=="POST":
                print("POST hitted")
                search_booked_vehicle = request.POST.get("search_booked_vehicle","").strip()
                print("search_booked_vehicle ::",search_booked_vehicle)
                if search_booked_vehicle:
                    vdata = vdata.filter(
                        Q(vehicle_id__buss_vehicle_company_name__icontains=search_booked_vehicle) |
                        Q(vehicle_id__buss_vehicle_model__icontains=search_booked_vehicle) |
                        Q(vehicle_id__buss_vehicle_color__icontains=search_booked_vehicle) |
                        Q(booking_date__icontains=search_booked_vehicle)
                    )

            
            vehicles = []
            service_charges = 250.0
            tax_percentage = 18
            for vehicle in vehicles:
                base_rental = float(vehicle.amount) 
                tax_amount = base_rental * tax_percentage / 100
                total_rental_amount = base_rental + service_charges + tax_amount

                vehicles.append({
                    'name': vehicle.name,
                    'base_rental': base_rental,
                    'service_charges': service_charges,
                    'tax_amount': tax_amount,
                    'total_rental_amount': total_rental_amount,
                })
            udata = usertable.objects.filter(id=uid)[0]
            context = {
                'vehicles': vehicles,
                'service_charges': service_charges,
                'tax_percentage': tax_percentage,
                "vdata": vdata, 
                "udata": udata
            }
            return render(request, "booking_history.html", context)
    except KeyError:
        vdata = "Please login!"
        udata = "Please login!"
    messages.error(request, vdata)
    return redirect("/")




# generate_receipt
from xhtml2pdf import pisa

# @csrf_exempt
def generate_rental_receipt(request):
    try:
        if request.session["log_id"]:
            uid = request.session["log_id"]
            log_user = request.session["log_user"]

            if request.method=="POST":
                booked_vid = request.POST["bookedid"]

            user=usertable.objects.get(id=uid)
            user_data = {

                "id":user.id,
                "fname": user.fname,
                "lname": user.fname,
                "email": user.emailid,
                "address_line1":user.address_line1,
                "phoneno": user.phonenum,
                "address_line1":user.address_line1,
                "city":user.city,
                "state":user.state,
                "zip_code":user.zip_code,
                "country":user.country
            }



            booked_vehicle_data=booking_table.objects.get(id=booked_vid)
            vehicle_data = {
                "vehicle_name": f'{booked_vehicle_data.vehicle_id.buss_vehicle_company_name} - {booked_vehicle_data.vehicle_id.buss_vehicle_model}',
                "vehicle_type": booked_vehicle_data.vehicle_id.buss_vehicle_type,
                # "registration_number": {{booked_vehicle_data.vehicle_id.}},
                "vehicle_color":  booked_vehicle_data.vehicle_id.buss_vehicle_color,
                "buss_vehicle_number":booked_vehicle_data.vehicle_id.buss_vehicle_number,
                
            }

            date_format = "%Y-%m-%d"
            from_date = datetime.strptime(str(booked_vehicle_data.from_duration), date_format)
            to_date = datetime.strptime(str(booked_vehicle_data.from_to), date_format)
            delta = to_date - from_date
            dayss = int(delta.days)
                
            base_rental = float(booked_vehicle_data.amount)
            service_charges = 250.00
            tax_percentage = 18
            total_rental_amount = base_rental + service_charges + (base_rental * tax_percentage / 100)

            booking_data = {
                "booking_id":booked_vehicle_data.id,
                "booking_date": booked_vehicle_data.booking_date,
                "from_duration": booked_vehicle_data.from_duration,
                "to_duration": booked_vehicle_data.from_to,
                "duration": dayss,
                "rental_amount":booked_vehicle_data.amount,
                "service_charges":250,
                "tax":"GST",
                "tax_per":18,
                "total_rental_amount": total_rental_amount,
            }
            pricing_data = {
                "base_price": "₹2500/day",
                "additional_charges": "₹500",
                "discount": "₹0",
                "total": "₹12,500",
            }
            payment_data = {
                "method": "Credit Card",
                "transaction_id": "TXN123456789",
            }
            context = {
                "user_data": user_data,
                "vehicle_data": vehicle_data,
                "booking_data": booking_data,
                "pricing_data": pricing_data,
                "payment_data": payment_data,
            }
            
            return render(request, "booking_receipt_generate.html", context)

    except KeyError:
        return redirect("booking_history")
    # return redirect("/")
    return redirect("booking_history")
    

# @csrf_exempt
# def download_generate_rental_receipt_as_pdf(request):
#     try:
#         if request.session["log_id"]:
#             uid = request.session["log_id"]
#             log_user = request.session["log_user"]
#             if request.method =="POST":
#                 # vd = request.POST.get("booked_id")
#                 booked_vehicle_id = request.POST["bookedid"]
#                 print("booked_vehicle_id :::",booked_vehicle_id)

                
#                 print("log_user :",log_user)
#                 # print("booked_vehicle_data :::",booked_vehicle_data)

#                 user=usertable.objects.get(id=uid)
#                 print("user ::",user)

#                 user_data = {
#                     "id":user.id,
#                     "fname": user.fname,
#                     "lname": user.fname,
#                     "email": user.emailid,
#                     "phoneno": user.phonenum,
#                     "address_line1":user.address_line1,
#                     "address_line1":user.address_line1,
#                     "city":user.city,
#                     "state":user.state,
#                     "zip_code":user.zip_code,
#                     "country":user.country

#                 }


#                 booked_vehicle_data=booking_table.objects.get(id=booked_vehicle_id)
#                 vehicle_data = {
#                     "vehicle_name": f'{booked_vehicle_data.vehicle_id.buss_vehicle_company_name} - {booked_vehicle_data.vehicle_id.buss_vehicle_model}',
#                     "vehicle_type": booked_vehicle_data.vehicle_id.buss_vehicle_type,
#                     # "registration_number": {{booked_vehicle_data.vehicle_id.}},
#                     "vehicle_color":  booked_vehicle_data.vehicle_id.buss_vehicle_color,
#                     "buss_vehicle_number":booked_vehicle_data.vehicle_id.buss_vehicle_number,
                    
#                 }

#                 date_format = "%Y-%m-%d"
#                 from_date = datetime.strptime(str(booked_vehicle_data.from_duration), date_format)
#                 to_date = datetime.strptime(str(booked_vehicle_data.from_to), date_format)
#                 delta = to_date - from_date
#                 dayss = int(delta.days)
                
#                 base_rental = float(booked_vehicle_data.amount)
#                 service_charges = 250.00
#                 tax_percentage = 18
#                 total_rental_amount = base_rental + service_charges + (base_rental * tax_percentage / 100)

#                 booking_data = {
#                     "booking_id":booked_vehicle_data.id,
#                     "booking_date": booked_vehicle_data.booking_date,
#                     "from_duration": booked_vehicle_data.from_duration,
#                     "to_duration": booked_vehicle_data.from_to,
#                     "duration": dayss,
#                     "rental_amount":booked_vehicle_data.amount,
#                     "service_charges":250,
#                     "tax":"GST",
#                     "tax_per":18,
#                     "total_rental_amount": total_rental_amount,
#                 }
#                 pricing_data = {
#                     "base_price": "₹2500/day",
#                     "additional_charges": "₹500",
#                     "discount": "₹0",
#                     "total": "₹12,500",
#                 }
#                 payment_data = {
#                     "method": "Credit Card",
#                     "transaction_id": "TXN123456789",
#                 }
#                 context = {
#                     "user_data": user_data,
#                     "vehicle_data": vehicle_data,
#                     "booking_data": booking_data,
#                     "pricing_data": pricing_data,
#                     "payment_data": payment_data,
#                 }

                
#                 html_content = render_to_string("booking_receipt_generate.html", context)

#                 response = HttpResponse(content_type="application/pdf")
#                 response['Content-Disposition'] = 'attachment; filename="rental_receipt.pdf"'

#                 pisa_status = pisa.CreatePDF(html_content, dest=response)

#                 if pisa_status.err:
#                     return HttpResponse("We had some errors while generating the PDF.")

#                 return response

#                 # return render(request, "booking_receipt_generate.html", context)

#     except KeyError:
#         return redirect("booking_history")
#     # return redirect("/")
#     return redirect("booking_history")

def download_generate_rental_receipt_as_pdf(request):
    try:
        if request.session.get("log_id"):
            uid = request.session["log_id"]
            log_user = request.session["log_user"]
            
            if request.method == "POST":
                booked_vehicle_id = request.POST["bookedid"]
                
                user = usertable.objects.get(id=uid)

                user_data = {
                    "id": user.id,
                    "fname": user.fname,
                    "lname": user.lname,
                    "email": user.emailid,
                    "phoneno": user.phonenum,
                    "address_line1": user.address_line1,
                    "address_line2": user.address_line2,
                    "city": user.city,
                    "state": user.state,
                    "zip_code": user.zip_code,
                    "country": user.country
                }

                booked_vehicle_data = booking_table.objects.get(id=booked_vehicle_id)
                vehicle_data = {
                    "vehicle_name": f'{booked_vehicle_data.vehicle_id.buss_vehicle_company_name} - {booked_vehicle_data.vehicle_id.buss_vehicle_model}',
                    "vehicle_type": booked_vehicle_data.vehicle_id.buss_vehicle_type,
                    "vehicle_color": booked_vehicle_data.vehicle_id.buss_vehicle_color,
                    "buss_vehicle_number": booked_vehicle_data.vehicle_id.buss_vehicle_number,
                }

                date_format = "%Y-%m-%d"
                from_date = datetime.strptime(str(booked_vehicle_data.from_duration), date_format)
                to_date = datetime.strptime(str(booked_vehicle_data.from_to), date_format)
                delta = to_date - from_date
                dayss = int(delta.days)
                
                base_rental = float(booked_vehicle_data.amount)
                service_charges = 250.00
                tax_percentage = 18
                total_rental_amount = base_rental + service_charges + (base_rental * tax_percentage / 100)

                booking_data = {
                    "booking_id": booked_vehicle_data.id,
                    "booking_date": booked_vehicle_data.booking_date,
                    "from_duration": booked_vehicle_data.from_duration,
                    "to_duration": booked_vehicle_data.from_to,
                    "duration": dayss,
                    "rental_amount": booked_vehicle_data.amount,
                    "service_charges": service_charges,
                    "tax": "GST",
                    "tax_per": tax_percentage,
                    "total_rental_amount": total_rental_amount,
                }

                # Create PDF Response
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="rental_receipt.pdf"'

                # Create the PDF canvas
                c = canvas.Canvas(response, pagesize=letter)
                width, height = letter

                # Header
                c.setFont("Helvetica", 14)
                c.drawString(30, height - 40, "Rental Receipt")
                c.setFont("Helvetica", 10)
                c.drawString(30, height - 60, "439 Rental Street, Ahmedabad, Gujarat, India")
                c.drawString(30, height - 75, "Phone: +916376094539")
                c.drawString(30, height - 90, "Email: starlettecars@gmail.com")
                c.setFillColor(colors.blue)
                c.drawString(30, height - 105, "Website: starlettecars.com")
                c.setFillColor(colors.black)

                # User Details
                c.setFont("Helvetica", 12)
                c.drawString(30, height - 140, "User Details:")
                c.setFont("Helvetica", 10)
                y_position = height - 155
                for key, value in user_data.items():
                    c.drawString(30, y_position, f"{key.replace('_', ' ').title()}: {value}")
                    y_position -= 15

                # Vehicle Details
                c.setFont("Helvetica", 12)
                c.drawString(30, y_position - 20, "Vehicle Details:")
                c.setFont("Helvetica", 10)
                y_position -= 35
                for key, value in vehicle_data.items():
                    c.drawString(30, y_position, f"{key.replace('_', ' ').title()}: {value}")
                    y_position -= 15

                # Booking Details
                c.setFont("Helvetica", 12)
                c.drawString(30, y_position - 20, "Booking Details:")
                c.setFont("Helvetica", 10)
                y_position -= 35
                for key, value in booking_data.items():
                    c.drawString(30, y_position, f"{key.replace('_', ' ').title()}: {value}")
                    y_position -= 15

                # Total Amount
                c.setFont("Helvetica-Bold", 12)
                c.drawString(30, y_position - 20, f"Total Amount: ₹{total_rental_amount}")

                # Footer
                c.setFont("Helvetica", 8)
                c.drawString(30, 30, "Thank you for choosing our service!")
                c.drawString(30, 15, "Contact us at starlettecars@gmail.com or +916376094539")

                # Save the PDF
                c.showPage()
                c.save()

                return response

    except KeyError:
        return redirect("booking_history")

    return redirect("booking_history")



def cancelbooking(request, id):
    print("cancelbooking id :::",id)
    try:
        boooking_history_data = booking_table.objects.get(id=id)

        boooking_history_data.is_cancelled = True
        boooking_history_data.cancelled_at = timezone.now()

        if boooking_history_data.vehicle_id.buss_vehicle_status == "Booked":
            boooking_history_data.vehicle_id.buss_vehicle_status = "Available"
            boooking_history_data.vehicle_id.save()
            print("boooking_history_data.vehicle_id.buss_vehicle_status.save()ed") 
        boooking_history_data.save()
        return redirect("/booking/history")
        # return render(request, "booking_history.html", {"boooking_history_data": boooking_history_data},)
    except booking_table.DoesNotExist:
        print("Booking not found.")
    except buss_vehicle.DoesNotExist:
        print("Vehicle not found.")
    except Exception as e:
        print("Exception RISED : ",e)
        pass
    return render(request,"booking_history.html",{"boooking_history_data": boooking_history_data})


# login form start ------
def showdata(request):
    if request.method == "POST":
        email = request.POST.get("email")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        password = request.POST.get("pass")
        rpassword = request.POST.get("rpass")
        # phoneno = request.POST.get("phone")
        # licence_no = request.POST.get("lnc_no")
        # address = request.POST.get("address")

        if (
            email == ""
            or fname == ""
            or lname == ""
            or password == ""
            or rpassword == ""
        ):
            messages.error(request, "Please Fill All Required Field.")

        elif password == rpassword:
            if usertable.objects.filter(fname=fname).exists():
                messages.info(
                    request, "Username Already Taken Please use Different username"
                )
                return redirect("/")
            elif usertable.objects.filter(emailid=email).exists():
                messages.info(request, "email should be unique, this email already registered.")
                return redirect("/")
            else:
                logindata = usertable(
                    fname=fname,
                    lname=lname,
                    emailid=email,
                    password=password,
                    # rpassword=rpassword,
                    role=2,
                    status=1,
                )
                logindata.save()
                messages.success(request, "Registartion done!")
                return redirect("accounts/success.html")

        else:
            messages.error(
                request, "Your Password and Confirm Password does not Matched!!"
            )
            return redirect("/")
    else:
        messages.error(request, "error occured!")

    return render(request, "index.html")

    #     elif password == rpassword:
    #         if usertable.objects.filter(name=name).exists():
    #             messages.info(request, "Username Already Taken")
    #             return redirect('index')
    #         elif usertable.objects.filter(emailid=email).exists():
    #             messages.info(request, "Email Already Taken")
    #             return redirect('index')
    #         else:
    #             logindata = usertable(emailid=email, phoneno=phoneno, password=password,rpassword=rpassword, name=name, licence_no=licence_no, address=address, role=2, status=1)
    #             logindata.save()
    #             messages.success(request, 'Registartion done!')
    #             print("User Created..")
    #             return redirect('index')
    #
    #     else:
    #         messages.error(request, 'Your Password and Confirm Password does not Matched!!')
    #         return redirect('index')
    # else:
    #     messages.error(request, 'error occured!')
    #
    # return render(request, 'index.html')


def checklogin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["upass"]
        if usertable.objects.filter(emailid=email).exists():
            try:
                user = usertable.objects.get(emailid=email, password=password)
                request.session["log_user"] = user.emailid
                request.session["log_id"] = user.id
                request.session.save()

            except usertable.DoesNotExist:
                user = None

            if user is not None:
                # return render(request,'index.html')
                print("User is Not None!!!")
                return redirect("/")

                # return render(request, "index.html")
                # return redirect('/myprofile')
                # return render(request,"Userprofile/myprofile.html")
            else:
                # print("Password does not matched!!!")
                messages.error(request, "Password does not matched!!!")
                # return render(request,'index.html')
                return redirect("/")

        else:
            messages.info(request, "account does not exist plz sign in")
            return redirect("/")
            # return render(request,'index.html')
    return render(request, "index.html")

    #     if usertable.objects.filter(emailid=email).exists():
    #         if usertable.objects.filter(password=password).exists():
    #             request.session['log_user'] = email
    #             request.session['log_id'] = password
    #             request.session.save()
    #             return redirect('index')
    #
    #         else:
    #             messages.error(request,"password is Invalid. You can try again..")
    #             return redirect('index')
    #     else:
    #         messages.info(request, 'account does not exit plz sign in')
    #         return redirect('index')
    # return render(request,'index.html')


# login form end ------


# contact form start -----
def contactdata(request):
    if request.method == "POST":

        name = request.POST.get("fname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("mess")

        logindata = contactus(
            email=email, phone=phone, message=message, name=name, contact_date="no"
        )
        logindata.save()
        messages.success(request, "Data has been submitted")
        # return redirect("/")
    else:
        messages.error(request, "error occurred!")

    # return render(request, "index.html")
    return redirect("/")


# contact form end --------



# myprofile
def myprofile(request):
    try:
        if request.session["log_id"]:
            loguser = request.session["log_user"]
            logid = request.session["log_id"]
            userdata = usertable.objects.filter(id=logid)[0]
        return render(request, "Userprofile/myprofile.html", {"userdata": userdata})
    except:
        userdata = "Please login!!"
        print(userdata)
        pass
    return redirect("/")


# def updateUserProfile(request):
#     if request.method =="POST":
#         try:
#             email = request.POST.get("email")
#             fname = request.POST.get("fname")
#             lname = request.POST.get("lname")
#             password = request.POST.get("pass")
#             rpassword = request.POST.get("rpass")
#             logindata = usertable(fname=fname, lname=lname, emailid=email, password=password, rpassword=rpassword, role=2, status=1)
#             logindata.save()
#         except:
#             pass
#     else:
#         messages.error("Error....you cann't update your Profile!!")


def inbox(request):
    try:
        if request.session["log_id"]:
            id = request.session["log_id"]
            userdata = request.session["log_user"]
            udata = usertable.objects.filter(id=id)[0]
    except KeyError:
        userdata = "Please login!!"
        udata = "Please login!!"
    data = usertable.objects.all()
    return render(request, "Userprofile/inbox.html", {"udata": udata})


def helps(request):
    try:
        if request.session["log_id"]:
            id = request.session["log_id"]
            userdata = request.session["log_user"]
            udata = usertable.objects.filter(id=id)[0]
    except KeyError:
        userdata = "Please login!!"
        udata = "Please login!!"
    return render(request, "Userprofile/helps.html", {"udata": udata})


def setting(request):
    try:
        if request.session["log_id"]:
            id = request.session["log_id"]
            userdata = request.session["log_user"]
            udata = usertable.objects.filter(id=id)[0]
    except KeyError:
        userdata = "Please login!!"
        udata = "Please login!!"
    return render(request, "Userprofile/settings.html", {"udata": udata})


def editprofile(request):
    try:
        loguser = request.session["log_user"]
        logid = request.session["log_id"]
        userdata = usertable.objects.filter(id=logid)[0]
        print("Edit profile page")
        # print("userdata image edit page :::",userdata.updProfile_photo)
        # print("userdata image :::",userdata.updProfile_image)
        return render(
            request, "Userprofile/editprofile/editprofile.html", {"userdata": userdata}
        )
    except:
        # print("Error Except!!!")
        pass

    # return render(request, "Userprofile/editprofile/editprofile.html",{"userdata":userdata})
    return redirect("/")


from django.core.validators import FileExtensionValidator


def updprofile(request):
    print("Update Profile page!!!!!!!!!1")
    try:
        if request.session["log_id"]:

            logid = request.session["log_id"]
            print("log_id ::",logid)
            userdata = usertable.objects.filter(id=logid)[0]
                    
            print("userdata ::",userdata)
            
            if request.method == "POST":
                print("POST!!!!!!!!!!!!!")
                try:
                    print("getting POST request !!!!!!!!")
                    updfname = request.POST["updfname"]
                    updlname = request.POST["updlname"]
                    updphonenum = request.POST["updphonenum"]

                    aadhaar_number = request.POST["aadhaar_number"]
                    date_of_birth = request.POST["date_of_birth"]
                    driver_license_number = request.POST["driver_license_number"]
                    driver_license_expiry = request.POST["driver_license_expiry"]
                    address_line1 = request.POST["address_line1"]
                    address_line2 = request.POST["address_line2"]
                    city = request.POST["city"]
                    state = request.POST["state"]
                    zip_code = request.POST["zip_code"]
                    country = request.POST["country"]



                    #update the user profile details
                    userdata.fname = updfname
                    userdata.lname = updlname
                    userdata.phonenum = updphonenum
                    userdata.date_of_birth = date_of_birth
                    print("date_of_birth :",date_of_birth)
                    userdata.aadhaar_number = aadhaar_number
                    userdata.driver_license_number = driver_license_number
                    userdata.driver_license_expiry = driver_license_expiry
                    print("driver_license_expiry :",driver_license_expiry)
                    userdata.address_line1 = address_line1
                    userdata.address_line2 = address_line2
                    userdata.city = city
                    userdata.state = state
                    userdata.zip_code = zip_code
                    userdata.country = country
                    userdata.save()
                    print("you profile have been updated!!!!")

                    try:
                        if request.method == "POST" and request.FILES.get("updProfileimg"):
                            print('request.method == "POST" and request.FILES.get("updProfileimg")')
                            updProfileimg = request.FILES["updProfileimg"]
                            userdata = usertable.objects.filter(id=logid)[0]
                            if updProfileimg:
                                # print("updProfileimg:::",updProfileimg)
                                valid_extensions = ["jpg", "jpeg", "png", "gif","webp"]
                                validator = FileExtensionValidator(
                                    allowed_extensions=valid_extensions,
                                    message="Please upload a valid image file.",
                                )
                                try:
                                    validator(updProfileimg)

                                except ValidationError as e:
                                    messages.error(request,"Please upload a valid image file.")
                                    return redirect("editprofile")

                                userdata.updProfile_photo = updProfileimg
                                userdata.save()
                                
                                # print("This is userdata.updProfile_photo ::",userdata.updProfile_photo)
                                # return render(request,"Userprofile/editprofile/editprofile.html",context)
                                return redirect("editprofile")
                            

                    except Exception as e:
                        print("Exception1 :",e)
                    
                    messages.success(request, "Your profile has been updated.")
                    return redirect("editprofile")

                except Exception as e:
                    print("This is BASE ECEPTION")
                    print("Exception2 :",e)
                    messages.error(request, f'{e}')
                    # print("You can't update your profile....error occurred")
                    pass

            return render(
                request, "Userprofile/editprofile/editprofile.html", {"userdata": userdata}
            )
        else:
            messages.error(request, "Profile login")
            return redirect("/")
    except Exception as e:
        print("Exception3 :",e)
        messages.error(request, f'{e}')
        pass

    return redirect("/")


def deleteprofileImg(request, id):
    try:
        udatax = usertable.objects.filter(id=id)
        userdatax = usertable.objects.get(id=id)
        delete_updProfile_photo = userdatax.updProfile_photo

        delete_updProfile_photo.delete()
        return redirect("editprofile")
    except:
        print("Exception RISED at deleteprofile!!")
        pass
    return render(
        request,
        "Userprofile/editprofile/editprofile.html",
        {"udata": udatax},
    )

def register(request):
    try:
        if request.session["log_id"]:
            print("already loggedIn ::register")
            return redirect("/")
    except:
        print("you are not loggedIn::register")
        pass

    if request.method == "POST":
        email = request.POST["email"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        password = request.POST["pass"]
        rpassword = request.POST["rpass"]
        # phoneno = request.POST["phone"]
        # licence_no = request.POST["lnc_no"]
        # address = request.POST["ddress"]

        if (
            email == ""
            or fname == ""
            or lname == ""
            or password == ""
            or rpassword == ""
        ):
            messages.error(request, "Please Fill All Required Field.")

        elif password == rpassword:
            if usertable.objects.filter(fname=fname).exists():
                messages.info(
                    request, "Username Already Taken Please use Different username"
                )
                # return redirect('/')
            elif usertable.objects.filter(emailid=email).exists():
                messages.info(request, "With this Email user Already Exist")
                # return redirect('/')
            else:
                auth_token = str(uuid.uuid4())
                registerdata = usertable(
                    fname=fname,
                    lname=lname,
                    emailid=email,
                    password=password,
                    # rpassword=rpassword,
                    auth_token=auth_token,
                    role=2,
                    status=1,
                )

                registerdata.save()
                print("data saved...")
                send_mail_after_registration(email, auth_token)

                user_mail_data = email

                messages.success(request, 'Registered successful!', extra_tags='registered_success')

                return render(request, "accounts/Verification_Token_Sended.html",{"associated_user": user_mail_data},)

        else:
            print("Your Password and Confirm Password does not Matched!!")
            messages.error(
                request, "Your Password and Confirm Password does not Matched!!"
            )
            # return redirect("/")
    # else:
    #     print("last error occured!")
        # messages.error(request, "error occured!")

    # print(str(uuid.uuid4()))
    # return render(request, "index.html")
    return render(request, "accounts/register.html")

def Resend_Email_Verification_Token(request):
    if request.method == 'POST':
        email = request.POST['email']
        print("resend email ::",email)
        if email:
            try:
                associated_user = usertable.objects.get(emailid=email)
                if associated_user:
                    if associated_user.is_verified:
                        messages.success(request, "Your account is already verified.")
                        return redirect("/")
                    auth_token = associated_user.auth_token
                    send_mail_after_registration(email, auth_token)
                    # messages.success(request, "Verification email resent successfully. Check your email.")
                # return redirect("login")
                user_mail_data = email
                return render(request, 'accounts/Verification_Token_Sended.html',{"associated_user": user_mail_data})  # Replace 'success' with the actual success URL
            except usertable.DoesNotExist:
                # Handle the case where the user with the provided email doesn't exist
                return render(request, 'accounts/verificationerror.html', {'error': 'Invalid email'})
    # return render(request, "accounts/Verification_Token_Sended.html")
    return redirect("login")

def send_mail_after_registration(email, auth_token):
    try:
        subject = "Your account needs to be varified."

        message = f"Please click on this link to varify your account. http://127.0.0.1:8000/accounts/verify/{auth_token}"
        send_from = settings.EMAIL_HOST_USER
        print("This is send from mail ::", send_from)
        recipient_list = [
            email,
        ]
        print("this is recipient_list ::", recipient_list)
        send_mail(
            subject,
            message,
            send_from,
            recipient_list,
            fail_silently=False,
        )
        print("send_mail done!!")
    except Exception as e:
        print("This is Exception..::", e)
        return False

    return True
    # return render("")

def verify(request, auth_token):
    try:
        registerdata = usertable.objects.filter(auth_token=auth_token).first()
        if registerdata:
            if registerdata.is_verified:
                messages.success(request, "Your account is already verified.")
                return redirect("login")
            registerdata.is_verified = True
            registerdata.save()
            messages.success(request, "Your Account has been varified.")
            return redirect("login")
        else:
            return redirect("verificationerror")
    except Exception as e:
        print(e)
    # return True


def verificationerror(request):
    return render(request, "accounts/verificationerror.html")

def login(request):
    try:
        if request.session["log_id"]:
            print("already loggedIn")
            return redirect("/")
    except Exception as e:
        pass

    if request.method == "POST":
        try:
            email = request.POST["email"]
            password = request.POST["upass"]
            
            if usertable.objects.filter(emailid=email).exists():
                user = usertable.objects.filter(emailid=email).first()
                
                if not user:    
                    messages.error(request, "Account does not exist. Please sign up.")
                    return render(request, "accounts/login.html")
                if not user.is_verified:
                    messages.error(request, "Please verify your account.")
                    return render(request, "accounts/login.html")
                if user.password == password:
                    # Successful login
                    request.session["log_user"] = user.emailid
                    request.session["log_id"] = user.id
                    user.update_last_login()
                    request.session.save()
                    messages.success(request, "Login successful!", extra_tags="login_success")
                    return redirect("/")
                else:
                    messages.error(request, "Invalid password. Please try again.")


                # if user_is.is_verified:
                #     try:
                #         user = usertable.objects.get(emailid=email, password=password)
                #         request.session["log_user"] = user.emailid
                #         request.session["log_id"] = user.id
                #         user.update_last_login()
                #         request.session.save()
                #         print("try user:::", user)
                #     except usertable.DoesNotExist:
                #         user = None
                #         print("exception user is None:", user)

                #     if user is not None:
                #         # return render(request,'index.html')
                #         print("User is Not None!!!")
                #         return redirect("/")
                #     else:
                #         messages.error(request, "Password does not matched!!!")
                #         print("Password does not matched!!!")
                # else:
                #     print("Please verify your account...")
                #     messages.error(request, "Please verify your account...")

            else:
                messages.error(request, "Account does not exist. Please sign up.")
                print("account does not exist plz sign in")
                # return redirect('/')
                return render(request, "accounts/login.html")
        except Exception as e:
            print("this is main Exception ::", e)
    print("login bottom!!!!!!!!")
    return render(request, "accounts/login.html")

# logout
def logout(request):
    try:
        del request.session["log_user"]
        del request.session["log_id"]
    except:
        pass
    return redirect("/")


# if user is already loggedIn to the site, he/she forgot or want to change their password to change password  ..
def change_pass(request):
    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        conf_password = request.POST["conf_password"]
        try:
            if request.session["log_id"]:
                id = request.session["log_id"]
                uid=usertable.objects.filter(id=id,password=old_password)
                if uid:
                    user_pass = usertable.objects.filter(id=id,password=old_password)[0]
                    
                    if user_pass:
                        if new_password == conf_password:
                            user_pass.password = new_password
                            user_pass.save()
                            # messages.error(request, "Your login password has been reset succesfuly.")
                            return redirect("pass_changed")

                        else:
                            messages.error(request, "new and confirm password does not matched..")

                else:
                    messages.error(request, "password is wrong..")
        except:
            user_pass = None
            messages.info(request, "if you forgot your password you can reset by entring your registered email, we will send you an password reset link for your registered account. thanks!")
            return redirect('resetpassword')

    return render(request, "Userprofile/editprofile/change_pass/change_pass.html")

def pass_changed(request):
    return render(request, "Userprofile/editprofile/change_pass/pass_changed.html")


# using email or phone otp
def reset_pass_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        token = str(uuid.uuid4())
        reset_pass_token = token
        try:
            associated_user = usertable.objects.get(emailid=email)
        except usertable.DoesNotExist:
            associated_user = None
        # associated_user = usertable.objects.filter(emailid=email)
        if associated_user:
            print("This is reset_pass_token ::",reset_pass_token)
            subject = "Change password for Starlettecars"
            plaintext = "change your password."
            htmltemp = f"<strong>Reset password</strong></br><p>A password change has been requested for your account. If this was you, please use the link below to reset your password. it will expires after 1 hour.</p></br> <p>http://127.0.0.1:8000/accounts/u/request/reset-password/token={reset_pass_token}<p>"
            try:
                msg = EmailMultiAlternatives(
                    subject,
                    plaintext,
                    "starlettecars@gmail.com",
                    [associated_user.emailid],
                    headers={"Reply-To": "starlettecars@gmail.com"},
                )
                msg.attach_alternative(htmltemp, "text/html")
                msg.send()
                # Create a new token
                # password_reset_token_expiration_time = usertable.objects.create(password_reset_token=reset_pass_token,password_reset_token_expiration_time=timezone.now() + timedelta(hours=1))
                associated_user.password_reset_token = reset_pass_token
                expiration_time = timezone.now() + timedelta(hours=1)
                associated_user.password_reset_token_expiration_time = expiration_time
                associated_user.save()
                # print("password_reset_token is save into database is:",reset_pass_token)
                reset_pass_page(request,reset_pass_token)
                                                  
                user_mail_data = associated_user
                reset_pass_request_mail_sended(request, user_mail_data)
            
            except BadHeaderError:
                return messages.error(request, "Invalid header found.")

            # messages.info(request, "Password reset instructions have been sented to your email.")
            return render(request,"accounts/reset_pass_request_mail_sended.html",{"associated_user": user_mail_data},)
            # return redirect("reset_pass_request_mail_sended",user_mail_data)
            # return render(request,"accounts/reset_pass_request.html")
        else:
            messages.error(request, "There is no user with that email address.")

    # print("this is resetpass!")
    return render(request, "accounts/reset_pass_request.html")

#verifing the password reset token that is sended thought mail.
def reset_pass_page(request,reset_pass_token):
    try:
        associated_user_pass_reset_token = usertable.objects.filter(password_reset_token=reset_pass_token)
        if associated_user_pass_reset_token:
            for data in associated_user_pass_reset_token:
                # print("data.password_reset_token ::",data.password_reset_token)
                if data.password_reset_token == reset_pass_token and data.is_password_reset_token_expired() is False:
                    if request.method == "POST":
                        new_upass=request.POST['new_upass']
                        conf_new_upass=request.POST['conf_new_upass']  
                        if new_upass == conf_new_upass:
                            # print("new_password and conf_password are equal...")
                            # print("associated_user_pass_reset_token :::",associated_user_pass_reset_token)
                            data.password = new_upass
                            data.save()
                            # print("pass saved..")
                            return redirect("pass_has_been_changed")
                            
                        else:
                            # print("password does not matched..")
                            messages.error(request, "confirm password does not matched..")
                else:
                    # print("token does not matched or expired!!")
                    return redirect("resetpassword")
        else:
            # print("Else error")
            return redirect("resetpassword")
            
    except Exception as e:
        # print(e)
        pass
    
    # print("ends:::")
    return render(request, "accounts/reset_pass_page.html")

def reset_pass_request_mail_sended(request, user_mail_data):
    user_mail_data = {user_mail_data: "user_mail_data"}
    return render(request, "accounts/reset_pass_request_mail_sended.html", user_mail_data)

def pass_has_been_changed(request):
    return render(request,"accounts/reset_pass_done.html")

# def success(request):
#     return render(request, "accounts/success.html")


from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework import generics
from .models import usertable
from .serializers import UsertableSerializer

class apix(generics.ListCreateAPIView):
    queryset = usertable.objects.all()
    serializer_class = UsertableSerializer

# def apix(request):

#     data = usertable.objects.all()
#     print(data)
#     print(type(data))

#     datax = {"data":data}
#     print(type(datax))

#     return JsonResponse(datax)




def generate_report(request):
    return render(request, "generate_report.html")


from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime


def generate_user_report(request):
    try:
        # Get start_date and end_date from the POST request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Filter users based on provided dates
        users = usertable.objects.all()
        booking_data = booking_table.objects.all()

        if start_date:
            parsed_start_date = parse_datetime(start_date)
            if not parsed_start_date:
                raise ValidationError("Invalid start date format.")
            users = users.filter(created_at__gte=parsed_start_date)
            booking_data = booking_data.filter(booking_date__gte=parsed_start_date)  # Assuming booking_date exists

        if end_date:
            parsed_end_date = parse_datetime(end_date)
            if not parsed_end_date:
                raise ValidationError("Invalid end date format.")
            users = users.filter(created_at__lte=parsed_end_date)
            booking_data = booking_data.filter(booking_date__lte=parsed_end_date)

        # Count the number of bookings
        booking_count = booking_data.count()

        # Pass the filtered users and booking count to the template
        context = {
            'users': users,
            'booking_count': booking_count,
        }

        return render(request, 'generate_user_report.html', context)

    except ValidationError as e:
        # Handle validation errors and pass the error message to the template
        return render(request, 'generate_user_report.html', {
            'error': str(e),
        })

    except Exception as e:
        # Handle any other exceptions and pass a generic error message to the template
        return render(request, 'generate_user_report.html', {
            'error': 'An error occurred.',
        })

    # If not a POST request, return an empty form or a default view
    return render(request, 'generate_user_report.html')



def export_user_report_in_pdf(request):
    try:
        # Get start_date and end_date from the POST request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        users = usertable.objects.all()

        if start_date:
            parsed_start_date = parse_datetime(start_date)
            if not parsed_start_date:
                raise ValidationError("Invalid start date format.")
            parsed_start_date = timezone.make_aware(parsed_start_date)  # Make timezone-aware
            users = users.filter(created_at__gte=parsed_start_date)

        if end_date:
            parsed_end_date = parse_datetime(end_date)
            if not parsed_end_date:
                raise ValidationError("Invalid end date format.")
            parsed_end_date = timezone.make_aware(parsed_end_date)  # Make timezone-aware
            users = users.filter(created_at__lte=parsed_end_date)

        # Create PDF response
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Add Logo
        logo_path = "media/reports/users/profile-user.png"  # Specify the path to your logo
        logo = Image(logo_path, width=0.5 * inch, height=0.5 * inch)
        elements.append(logo)
        elements.append(Spacer(1, 12))  # Add some space below the logo
        
        # Title
        styles = getSampleStyleSheet()
        title = Paragraph("User Report", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 20))

        current_datetime = datetime.now().strftime("%B %d, %Y, %I:%M:%S %p")  # e.g., "October 15, 2024, 07:16:17 PM"
        generated_on = Paragraph(f"Generated on: {current_datetime}", styles['Normal'])
        elements.append(generated_on)

        description_style = ParagraphStyle(
            'DescriptionStyle',
            parent=styles['Normal'],
            spaceBefore=12,
            spaceAfter=12,
        )
        description = Paragraph("This report contains user data filtered by registration date.", description_style)
        elements.append(description)

        # Filter date information
        filterdate_style = ParagraphStyle(
            'FilterdateStyle',
            parent=styles['Normal'],
            spaceBefore=12,
            spaceAfter=12,
            fontSize=10,
        )
        filterdate = Paragraph(f"From - {start_date} To - {end_date}", filterdate_style)
        elements.append(filterdate)

        # Table data preparation
        data = [['First Name', 'Last Name', 'Email', 'Phone Number', 'Date of Birth', 'Created At']]  # Table headers
        # , 'City', 'State','Zip Code'
        # Add user data to the table
        for user in users:
            data.append([user.fname, user.lname, user.emailid, user.phonenum, user.date_of_birth, str(user.created_at.date())])
            # , user.city, user.state, user.zip_code

        # Create the table
        table = Table(data)

        # Style the table
        style = TableStyle([ 
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(242/255, 242/255, 242/255)),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.Color(50/255, 50/255, 50/255)),      # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically align all cells in the middle
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Padding for header row
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Body background color
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),  # Grid lines for the table
        ])

        table.setStyle(style)
        elements.append(Spacer(1, 12))  # Spacer for better layout
        elements.append(table)
        elements.append(Spacer(1, 20))  # Spacer after the table

        # Add concluding statement
        conclusion_style = ParagraphStyle(
            'ConclusionStyle',
            parent=styles['Normal'],
            spaceBefore=12,
            spaceAfter=12,
        )
        conclusion = Paragraph("Thank you for reviewing this report. For any further inquiries, please contact us.", conclusion_style)
        elements.append(conclusion)

        # Build the PDF
        doc.build(elements)

        # Get PDF from the buffer
        pdf = buffer.getvalue()
        buffer.close()

        # Create HTTP response with PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="user_report.pdf"'

        return response

    except ValidationError as e:
        return HttpResponse("Invalid date format", status=400)  # Return HTTP 400 for validation errors

    except Exception as e:
        return HttpResponse("An error occurred.", status=500)  # Return HTTP 500 for other errors
    


import csv

def export_user_report_in_csv(request):
    try:
        # Prepare HTTP response with the correct content type for CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_report.csv"'

        # Create a CSV writer object
        writer = csv.writer(response)

        # Write the header row
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone Number', 'Created At'])

        # Retrieve query parameters for filtering
        start_date = request.GET.get('start_date')  # Use GET for query params
        end_date = request.GET.get('end_date')

        # Filter users based on provided dates
        users = usertable.objects.all()

        if start_date:
            parsed_start_date = parse_datetime(start_date)
            if parsed_start_date:
                users = users.filter(created_at__gte=parsed_start_date)

        if end_date:
            parsed_end_date = parse_datetime(end_date)
            if parsed_end_date:
                users = users.filter(created_at__lte=parsed_end_date)

        # Write user data to CSV
        for user in users.values_list('fname', 'lname', 'emailid', 'phonenum', 'created_at'):
            writer.writerow(user)

        return response  # Return the CSV response directly

    except Exception as e:
        # Handle any errors that occur
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    




# Vehicle Report 

def generate_vehicle_report(request):
    try:
        # Retrieve query parameters for filtering
        start_date = request.GET.get('start_date')  # Use GET for query params
        end_date = request.GET.get('end_date')

        # Filter vehicles based on provided dates
        get_vehicle_data = buss_vehicle.objects.all()

        if start_date:
            parsed_start_date = parse_datetime(start_date)
            if not parsed_start_date:
                raise ValidationError("Invalid start date format.")
            get_vehicle_data = get_vehicle_data.filter(buss_vehicle_registered_at__gte=parsed_start_date)

        if end_date:
            parsed_end_date = parse_datetime(end_date)
            if not parsed_end_date:
                raise ValidationError("Invalid end date format.")
            get_vehicle_data = get_vehicle_data.filter(buss_vehicle_registered_at__lte=parsed_end_date)

        # Prepare context for rendering
        context = {
            'vehicles': get_vehicle_data,
            'start_date': start_date,
            'end_date': end_date,
        }

        # Render the template with filtered vehicle data
        return render(request, "generate_vehicle_report.html", context)
    
    except ValidationError as e:
        # Handle validation errors and pass the error message to the template
        return render(request, 'generate_vehicle_report.html', {
            'error': str(e),
        })

    except Exception as e:
        # Handle any other exceptions and pass a generic error message to the template
        return render(request, 'generate_vehicle_report.html', {
            'error': 'An error occurred.',
        })
    





def export_vehicle_report_in_pdf(request):
    try:
        # Retrieve query parameters for filtering
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Filter vehicles based on date range
        vehicles = buss_vehicle.objects.all()
        if start_date:
            vehicles = vehicles.filter(buss_vehicle_registered_at__gte=start_date)
        if end_date:
            vehicles = vehicles.filter(buss_vehicle_registered_at__lte=end_date)

        # Create a PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(letter),
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=18,
        )
        elements = []

        # Add logo (optional)
        logo_path = os.path.join('media/reports/vehicle_Reports_Icon', 'profile-user.png')
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=1 * inch, height=1 * inch)
            elements.append(logo)

        # Add title and header styling
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Title'],
            fontSize=20,
            alignment=1,  # Center alignment
            spaceAfter=20
        )
        title = Paragraph("Company Vehicle Report", title_style)
        elements.append(title)

        # Add generated date
        current_datetime = datetime.now().strftime("%B %d, %Y, %I:%M:%S %p")
        generated_on = Paragraph(f"Generated on: {current_datetime}", styles['Normal'])
        elements.append(generated_on)
        elements.append(Spacer(1, 12))

        # Add filter description
        filter_info = "Filters applied: "
        if start_date and end_date:
            filter_info += f"From {start_date} to {end_date}"
        elif start_date:
            filter_info += f"From {start_date} onward"
        elif end_date:
            filter_info += f"Up to {end_date}"
        else:
            filter_info += "No filters applied"
        elements.append(Paragraph(filter_info, styles['Normal']))
        elements.append(Spacer(1, 20))

        # Prepare table data
        table_data = [
            ['Vehicle ID', 'Owner Email', 'Company', 'Model', 'Color', 'Type', 'Location', 'Rent Per Day']
        ]

        for vehicle in vehicles:
            table_data.append([
                vehicle.id,
                vehicle.buss_vehicle_owner.buss_emailid if vehicle.buss_vehicle_owner else "N/A",
                vehicle.buss_vehicle_company_name,
                vehicle.buss_vehicle_model,
                vehicle.buss_vehicle_color,
                vehicle.buss_vehicle_type,
                vehicle.buss_vehicle_location,
                f'${float(vehicle.buss_rent_per_day):.2f}' if vehicle.buss_rent_per_day else "N/A"
            ])

        # Define column widths dynamically
        col_widths = [
            1.2 * inch,  # Vehicle ID
            2 * inch,    # Owner Email
            1.5 * inch,  # Company
            1.5 * inch,  # Model
            1 * inch,    # Color
            1.2 * inch,  # Type
            1.5 * inch,  # Location
            1.2 * inch,  # Rent Per Day
        ]

        # Create table
        table = Table(table_data, colWidths=col_widths)
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f2f2f2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#323232")),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d1d1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ])
        table.setStyle(table_style)

        elements.append(KeepTogether(table))
        elements.append(Spacer(1, 20))

        # Footer with page number
        footer = Paragraph(
            "This report is generated by Starlettecars. Page: 1",
            ParagraphStyle('FooterStyle', parent=styles['Normal'], fontSize=10, alignment=1)
        )
        elements.append(Spacer(1, 10))
        elements.append(footer)

        # Build PDF
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        # Return response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="vehicle_report.pdf"'
        return response

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
 

from openpyxl import Workbook

def export_vehicle_report_in_excel(request):
    try:
        # Retrieve query parameters for filtering
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Filter vehicles based on date range
        vehicles = buss_vehicle.objects.all()
        if start_date:
            vehicles = vehicles.filter(buss_vehicle_registered_at__gte=start_date)
        if end_date:
            vehicles = vehicles.filter(buss_vehicle_registered_at__lte=end_date)

        # Generate current date-time
        current_datetime = datetime.now().strftime("%B %d, %Y, %I:%M:%S %p")

        # Create an Excel workbook
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Vehicle Report"

        # Add generated date at the top of the sheet
        sheet.append([f"Generated on: {current_datetime}"])

        # Leave a blank row for better readability
        sheet.append([])

        # Add filter information
        if start_date or end_date:
            if start_date and end_date:
                sheet.append([f"All registered vehicles between {start_date} and {end_date}"])
            elif start_date:
                sheet.append([f"All registered vehicles from {start_date} onwards"])
            elif end_date:
                sheet.append([f"All registered vehicles up to {end_date}"])
        else:
            sheet.append([f"All registered vehicles as of {current_datetime}"])

        # Leave another blank row for separation
        sheet.append([])

        # Add headers
        headers = [
            'Vehicle ID', 'Vehicle Owner Email', 'Company', 'Model', 'Color',
            'Type', 'Location', 'Rent Per Day', 'Discounted Rent'
        ]
        sheet.append(headers)

        # Add vehicle data
        for vehicle in vehicles:
            owner_email = vehicle.buss_vehicle_owner.buss_emailid if vehicle.buss_vehicle_owner else "N/A"
            sheet.append([
                vehicle.id,
                owner_email,
                vehicle.buss_vehicle_company_name,
                vehicle.buss_vehicle_model,
                vehicle.buss_vehicle_color,
                vehicle.buss_vehicle_type,
                vehicle.buss_vehicle_location,
                f'${float(vehicle.buss_rent_per_day):.2f}' if vehicle.buss_rent_per_day else "N/A"
            
            ])

        # Create an HTTP response with the Excel file
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="vehicle_report.xlsx"'
        workbook.save(response)

        return response

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
def generate_booked_vehicle_report(request):
    try:
        # Retrieve query parameters for filtering
        start_date = request.GET.get('start_date')  # Use GET for query params
        end_date = request.GET.get('end_date')

        # Filter vehicles based on provided dates
        get_vehicle_data = booking_table.objects.all()

        # if start_date:
        #     parsed_start_date = parse_datetime(start_date)
        #     if not parsed_start_date:
        #         raise ValidationError("Invalid start date format.")
        #     get_vehicle_data = get_vehicle_data.filter(buss_vehicle_registered_at__gte=parsed_start_date)

        # if end_date:
        #     parsed_end_date = parse_datetime(end_date)
        #     if not parsed_end_date:
        #         raise ValidationError("Invalid end date format.")
        #     get_vehicle_data = get_vehicle_data.filter(buss_vehicle_registered_at__lte=parsed_end_date)

        # Prepare context for rendering
        context = {
            'vehicles': get_vehicle_data,
            'start_date': start_date,
            'end_date': end_date,
        }

        # Render the template with filtered vehicle data
        return render(request, "generate_booked_vehicle_report.html", context)
    
    except ValidationError as e:
        # Handle validation errors and pass the error message to the template
        return render(request, 'generate_booked_vehicle_report.html', {
            'error': str(e),
        })

    except Exception as e:
        # Handle any other exceptions and pass a generic error message to the template
        return render(request, 'generate_booked_vehicle_report.html', {
            'error': 'An error occurred.',
        })
    
