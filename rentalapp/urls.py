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
    path('vehicle/booking/generate-receipt', views.generate_rental_receipt, name='rental_receipt'),
    path('vehicle/booking/download_generate_rental_receipt_as_pdf', views.download_generate_rental_receipt_as_pdf, name='download_generate_rental_receipt_as_pdf'),
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
    # path("accounts/success", views.success, name="success"),
    # path("accounts/verify/email", views.EmailVerificationTokenSended, name="EmailVerificationTokenSended"),
    path("accounts/verify/<slug:auth_token>", views.verify, name="verify"),
    path("accounts/verify/email/resend", views.Resend_Email_Verification_Token, name="Resend_Email_Verification_Token"),
    path("accounts/verification/error=??", views.verificationerror, name="verificationerror",), 


    # Report
    path("generate/report", views.generate_report, name="generate_report",),

    path("generate/user/report", views.generate_user_report, name="generate_user_report",),
    # http://127.0.0.1:8000/api/get/user-report/?start_date=2024-10-11&end_date=2024-10-14
    path('export/user/report/in/pdf/', views.export_user_report_in_pdf, name='export_user_report_in_pdf'),
    # http://127.0.0.1:8000/api/export/user-report/in/pdf/?start_date=2024-10-11&end_date=2024-10-14
    path('export/user/report/in/csv/', views.export_user_report_in_csv, name='export_user_report_in_csv'),
    # http://127.0.0.1:8000/api/export/user-report/in/csv/?start_date=2024-10-11&end_date=2024-10-14



    path("generate/vehicle/report", views.generate_vehicle_report, name="generate_vehicle_report",),
    # export_vehicle_report_in_pdf
    path('export/vehicle/report/in/pdf/', views.export_vehicle_report_in_pdf, name='export_vehicle_report_in_pdf'),
    path('export/vehicle/report/in/csv/', views.export_vehicle_report_in_excel, name='export_vehicle_report_in_excel'),


    # /generate/booked/vehicle/report
    path("generate/booked/vehicle/report", views.generate_booked_vehicle_report, name="generate_booked_vehicle_report",),

    path("apix", views.apix.as_view(), name="apix"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
