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
from django.core.mail import send_mail


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

    for i in range(1, len(fetchvehicle) + 1):
        if i <= len(vlist):
            x = random.sample(vlist, i)

    return render(request,"index.html",{"vehicle": fetchvehicle, "x": x, "udata": udata, "userdata": userdata})


def termsandconpage(request):
    return render(request, "termsandconpage.html")

def services(request):
    try:
        if request.session["log_id"]:
            id = request.session["log_id"]
            userdata = request.session["log_user"]
            udata = usertable.objects.filter(id=id)[0]
    except KeyError:
        userdata = "Please login!!"
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
    ## This is for random vehicle values
    vlist = list(fetchvehicle)
    
    for i in range(1, len(fetchvehicle) + 1):
        if i <= len(vlist):
            x = random.sample(vlist, i)
    # x = list(buss_vehicle.objects.all())
    # x = random.sample(x, 9)
    return render(
        request, "vehicles.html", {"vehicle": fetchvehicle, "x": x, "udata": udata}
    )


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
    print("inside the vehicle booking")
    if request.method == "POST":
        try:
            if request.session["log_id"]:
                from_duration = request.POST.get("sdate")
                to_duration = request.POST.get("edate")
                uid = request.session["log_id"]
                vid = request.POST.get("vid")
                rupee = request.POST.get("rupee")
                

                date_format = "%Y-%m-%d"
                from_date = datetime.strptime(str(from_duration), date_format)
                to_date = datetime.strptime(str(to_duration), date_format)
                today = datetime.today().date()
                current_date =datetime.strptime(str(today), date_format)
                
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
                    vehicle_status = buss_vehicle.objects.get(id=vid)
                    print("vehicle_status.id" ,id)
                    print("vehicle_status.vid" ,vid)
                    if vehicle_status.buss_vehicle_status == "Booked":
                        messages.success(request, "This Vehicle is Already Booked by an another user!")
                        print("redirected same vehicle page....")
                        # return redirect("/booking/history")
                    if vehicle_status.buss_vehicle_status == "Under Maintenance":
                        messages.success(request, "This Vehicle is in Under Maintenance!")
                        print("redirected same vehicle page....")
                    if vehicle_status.buss_vehicle_status == "Out of Service":
                        messages.success(request, "This Vehicle is Out of Service!")
                        print("redirected same vehicle page....")


                    if vehicle_status.buss_vehicle_status == "Available":
                        vehicle_status.buss_vehicle_status = "Booked"
                        vehicle_status.save()

                        bookingdata = booking_table(
                            amount=amount,
                            from_to=to_duration,
                            from_duration=from_duration,
                            login_id=usertable(id=uid),
                            vehicle_id=buss_vehicle(id=vid), #, buss_vehicle_status=vehicle_status
                            paystatus=1,
                        )
                        bookingdata.save()
                        messages.success(request, "Booking Done!")
                        print("redirected to booking history page....")
                        return redirect("/booking/history")
                else:
                    # fetch = buss_vehicle.objects.get(vid=vid)
                    messages.error(request, "Please Enter a Valid Date Formate!!!")
            else:
                print("session log_id are not available!!")
        except KeyError:
            print("please login to continue.....")
            messages.error(request,"please login...")
            pass
    else:
        # messages.error(request, "error occured!")
        print("error occured!")

    vid = request.POST.get("vid")
    return redirect("checkout/{}".format(vid))


# @login_required()
def booking_history(request):
    try:
        if request.session["log_id"]:
            uid = request.session["log_id"]
            vdata = booking_table.objects.filter(login_id=uid)
            # print("vdata is s ss :",vdata)
            udata = usertable.objects.filter(id=uid)[0]

            return render(request, "booking_history.html", {"vdata": vdata, "udata": udata})
    except KeyError:
        vdata = "Please login!"
        udata = "Please login!"
    messages.error(request, vdata)
    return redirect("/")

def cancelbooking(request, id):
    print("cancelbooking id :::",id)
    try:
        boooking_history_data = booking_table.objects.get(id=id)
        # if request.method == 'POST':
        print("vdata is :",boooking_history_data)
        # boooking_history_data
        print("vdata is :",boooking_history_data.paystatus)
        boooking_history_data.is_cancelled = True
        boooking_history_data.cancelled_at = timezone.now()
        boooking_history_data.save()
        print("boooking_history_data.save()ed")            
    
        if boooking_history_data.vehicle_id.buss_vehicle_status == "Booked":
            boooking_history_data.vehicle_id.buss_vehicle_status = "Available"
            boooking_history_data.vehicle_id.save()
            print("boooking_history_data.vehicle_id.buss_vehicle_status.save()ed") 

        # cancelbooking.delete()
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
                messages.info(request, "With this Email user Already Exist")
                return redirect("/")
            else:
                logindata = usertable(
                    fname=fname,
                    lname=lname,
                    emailid=email,
                    password=password,
                    rpassword=rpassword,
                    role=2,
                    status=1,
                )
                logindata.save()
                messages.success(request, "Registartion done!")
                return redirect("/")

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


def feedbackshow(request):
    try:
        if request.method == "POST":
            if request.session["log_id"]:
                name = request.POST.get("name")
                comment = request.POST.get("comments")
                ratings = request.POST.get("rating1")
                uid = request.session["log_id"]
                feedbackdata = feedback(
                    name=name, comments=comment, l_id=usertable(id=uid), ratings=ratings
                )  # l_id=usertable(id=uid)
                feedbackdata.save()
                messages.success(request, "feedback has been submitted!")
                return redirect("/feedback")
            else:
                messages.success(request, "please login for giving feedback")
        # else:
        #     print("request.method is not POST")
    except Exception as e:
        print("exception is :",e)
        messages.error(request, "please login for giving feedback!")

    return redirect("/feedback")


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
    try:
        if request.method == "POST":
            try:
                updfname = request.POST["updfname"]
                updlname = request.POST["updlname"]
                updphonenum = request.POST["updphonenum"]
                # updpassword = request.POST["updpassword"]
                # updrpassword = request.POST["updrpassword"]

                logid = request.session["log_id"]
                userdata = usertable.objects.filter(id=logid)[0]
                userdata.fname = updfname
                userdata.lname = updlname
                userdata.phonenum = updphonenum
                userdata.save()

                try:
                    if request.method == "POST" and request.FILES.get("updProfileimg"):
                        updProfileimg = request.FILES["updProfileimg"]
                        userdata = usertable.objects.filter(id=logid)[0]
                        if updProfileimg:
                            # print("updProfileimg:::",updProfileimg)
                            valid_extensions = ["jpg", "jpeg", "png", "gif"]
                            validator = FileExtensionValidator(
                                allowed_extensions=valid_extensions,
                                message="Please upload a valid image file.",
                            )
                            try:
                                validator(updProfileimg)

                            except ValidationError as e:
                                context = {
                                    "userdata": userdata,
                                    "messagess": e.message,
                                }
                                return render(
                                    request,
                                    "Userprofile/editprofile/editprofile.html",
                                    context,
                                )

                            userdata.updProfile_photo = updProfileimg
                            userdata.save()
                            # print("This is Saved....")
                            # print("This is userdata.updProfile_photo ::",userdata.updProfile_photo)
                            # return render(request,"Userprofile/editprofile/editprofile.html",context)
                            return redirect("editprofile")
                except:
                    pass
                messages.success(request, "Your profile has been updated.")
                return redirect("editprofile")

            except:
                # print("This is BASE ECEPTION")
                # print("You can't update your profile....error occurred")
                pass

        else:
            # print("This is Else of updateprofile Error occurred!! ")
            messages.error(request, "Error....you cann't update your Profile!!")
            return render(request, "Userprofile/editprofile/editprofile.html")
    except:
        # print("This is MAIN ECEPTION occurred")
        pass
    # print("!!!! This is after if !!!!")
    logid = request.session["log_id"]
    userdata = usertable.objects.filter(id=logid)[0]

    return render(
        request, "Userprofile/editprofile/editprofile.html", {"userdata": userdata}
    )


def deleteprofile(request, id):
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


def login(request):
    try:
        if request.session["log_id"]:
            print("already loggedIn")
            return redirect("/")
    except Exception as e:
        print("exception you are not loggedIn::???", e)
        pass

    if request.method == "POST":
        try:
            email = request.POST["email"]
            password = request.POST["upass"]
            if usertable.objects.filter(emailid=email).exists():
                user_is = usertable.objects.filter(emailid=email).first()
                if user_is.is_verified:
                    try:
                        user = usertable.objects.get(emailid=email, password=password)
                        request.session["log_user"] = user.emailid
                        request.session["log_id"] = user.id
                        request.session.save()
                        print("try user:::", user)
                    except usertable.DoesNotExist:
                        user = None
                        print("exception user is None:", user)

                    if user is not None:
                        # return render(request,'index.html')
                        print("User is Not None!!!")
                        return redirect("/")
                    else:
                        messages.error(request, "Password does not matched!!!")
                        print("Password does not matched!!!")
                else:
                    print("Please verify your account...")
                    messages.error(request, "Please verify your account...")

            else:
                messages.info(request, "account does not exist plz sign in")
                print("account does not exist plz sign in")
                # return redirect('/')
                return render(request, "accounts/login.html")
        except Exception as e:
            print("this is main Exception ::", e)
    print("login bottom!!!!!!!!")
    return render(request, "accounts/login.html")


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
                    rpassword=rpassword,
                    auth_token=auth_token,
                    role=2,
                    status=1,
                )

                registerdata.save()
                print("data saved...")
                send_mail_after_registration(email, auth_token)
                print(
                    "Registartion done go to login page! send_mail_after_registration..."
                )
                messages.success(request, "Registartion done go to login page!")
                return redirect("token_send")

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
    return render(request, "accounts/register.html")

# logout
def logout(request):
    try:
        del request.session["log_user"]
        del request.session["log_id"]
    except:
        pass
    return redirect("/")

def send_mail_after_registration(email, auth_token):
    try:
        subject = "Your account needs to be varified."

        message = f"Hi paste the link to varify your account. http://192.168.43.69:8000/accounts/verify/{auth_token}"
        send_from = settings.EMAIL_HOST_USER
        print("This is send from maill ::", send_from)
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


# if user is already loggedIn to the site, he/she forgot or want to change their password to change password  ..
def change_pass(request):
    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        conf_password = request.POST["conf_password"]
        try:
            if request.session["log_id"]:
                id = request.session["log_id"]
                user_pass = usertable.objects.filter(password=old_password, id=id)[0]
                # print("this is user_pass", user_pass)

            if new_password == conf_password:
                # print("new_password and conf_password are equal...")
                # user_pass = usertable.objects.filter(password=old_password, id=id)
                user_pass.password = new_password
                user_pass.rpassword = conf_password
                user_pass.save()
                # print("pass saved..")
                return redirect("pass_changed")

            else:
                # print("password does not matched..")
                messages.error(request, " new and confirm password does not matched..")
        except:
            user_pass = None
            # print("Exception!!!")
            messages.error(request, "your old password is wrong..")

        # except usertable.DoesNotExist:
        #     user_pass = None
        #     print("Exception!!!")

    return render(request, "Userprofile/editprofile/change_pass/change_pass.html")
    # return redirect("/")


def pass_changed(request):
    return render(request, "Userprofile/editprofile/change_pass/pass_changed.html")


# using mail or phone otp
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
            htmltemp = f"<strong>Reset password</strong></br><p>A password change has been requested for your account. If this was you, please use the link below to reset your password. it will expires after 1 hour.</p></br> <p>http://192.168.43.69:8000/accounts/u/request/reset-password/token={reset_pass_token}<p>"
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
                            data.rpassword = conf_new_upass
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

def success(request):
    return render(request, "accounts/success.html")


def token_send(request):
    return render(request, "accounts/token_send.html")
