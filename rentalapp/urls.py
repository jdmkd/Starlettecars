from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index),
    path("index/", views.index, name="index"),
    path("services", views.services),
    path("vehicles", views.vehicles),
    path("showdata", views.showdata),
    path("checklogin", views.checklogin),
    path("logout", views.logout),
    path("contact", views.contact),
    path("contactdata", views.contactdata),
    path("feedback", views.feedbackpage),
    path("feedbackshow", views.feedbackshow),

    path("checkoutform", views.checkoutform),
    path("vehicle/checkout/<int:id>", views.checkout, name="vehicle_checkout"),
    path("vehicle/booking", views.vehicle_booking, name="vehicle_booking"),
    path("booking/history", views.booking_history, name="booking_history"),
    path("cancelbooking/<int:id>", views.cancelbooking, name="cancelbooking"),
    path("termsandconpage", views.termsandconpage),
    path("inbox", views.inbox),
    path("helps", views.helps),
    path("settings", views.setting),
    path("accounts/myprofile", views.myprofile, name="myprofile"),
    path("accounts/myprofile/editprofile", views.editprofile, name="editprofile"),
    path("accounts/myprofile/updprofile", views.updprofile, name="updprofile"),
    path("accounts/myprofile/deleteprofile/<int:id>", views.deleteprofileImg, name="deleteprofileImg"),
    # if user is already loggedIn to the site, he/she forgot or want to change their password to change password  ..
    path("accounts/myprofile/editprofile/change_password", views.change_pass, name="change_password"),
    path("accounts/myprofile/editprofile/pass_changed", views.pass_changed, name="pass_changed"),
    # end edit password
    # if user forgot password and does not loggedIn to site for reset password
    path("accounts/reset_password", views.reset_pass_request, name="resetpassword"),
    path("accounts/resetpassword/request/mail_sended/<slug:user_mail_data>",views.reset_pass_request_mail_sended,
        name="reset_pass_request_mail_sended",
    ),
    path(
        "accounts/u/request/reset-password/token=<slug:reset_pass_token>",views.reset_pass_page,
        name="reset_pass_page",
    ),
    path(
        "accounts/u/request/reset-password/pass-has-been-changed",views.pass_has_been_changed,
        name="pass_has_been_changed",
    ),
    
    path("accounts/login", views.login, name="login"),
    path("accounts/register", views.register, name="register_attempt"),
    path("accounts/success", views.success, name="success"),
    # path("accounts/verify/email", views.EmailVerificationTokenSended, name="EmailVerificationTokenSended"),
    path("accounts/verify/<slug:auth_token>", views.verify, name="verify"),
    path("accounts/verify/email/resend", views.Resend_Email_Verification_Token, name="Resend_Email_Verification_Token"),
    path("accounts/verification/error=??", views.verificationerror, name="verificationerror",),


    path("apix", views.apix.as_view(), name="apix"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
