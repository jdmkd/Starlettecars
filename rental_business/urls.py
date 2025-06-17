from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("registered/vehicles", views.registered_vehicles, name="registered_vehicles"),
    path("registered/vehicle/details", views.registered_vehicle_details, name="registered_vehicle_details"),
    path("registered/vehicle/details/update", views.registered_vehicle_details_update, name="registered_vehicle_details_update"),
    path("registered/vehicle/details/update/done", views.registered_vehicle_details_update_done, name="registered_vehicle_details_update_done"),




    path("login_and_registration", views.login_and_registration, name="login_and_registration"),
    
    path("buss_logout", views.buss_logout, name="buss_logout"),
    path("buss_login", views.buss_login, name="buss_login"),
    path("buss_registeration", views.buss_registeration, name="buss_registeration"),
    path("email_verify/<slug:buss_auth_token>", views.email_verify, name="email_verification"),
    path("accounts/verify/email", views.mail_token_send, name="mail_token_send"),
    path("verificationerror", views.verificationerror, name="verificationerror"),
    path("add_vehicle",views.add_vehicle, name="add_vehicle"),


    path("vehicle/booking/approval",views.vehicle_booking_approval,name="vehicle_booking_approval"),
    path("vehicle/booking/approval/view/user/detail",views.view_user_detail_for_approval,name="view_user_detail_for_approval"),


    path("business/accounts/myprofile",views.buss_profile, name="buss_profile"),
    path("business/accounts/myprofile/edit",views.buss_profile_edit, name="buss_profile_edit"),


    # path("dashboard",views.dashboard, name="dashboard"),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
