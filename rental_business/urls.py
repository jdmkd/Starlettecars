from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.buss_index, name="buss_index"),
    path("buss_index", views.buss_index, name="buss_index"),
    path("login_and_registration", views.login_and_registration, name="login_and_registration"),
    
    path("buss_logout", views.buss_logout, name="buss_logout"),
    path("buss_login", views.buss_login, name="buss_login"),
    path("buss_registeration", views.buss_registeration, name="buss_registeration"),
    path("email_verify/<slug:buss_auth_token>", views.email_verify, name="email_verification"),
    path("accounts/verify/email", views.mail_token_send, name="mail_token_send"),
    path("verificationerror", views.verificationerror, name="verificationerror"),

    path("add_new_vehicle",views.add_new_vehicle,name="add_new_vehicle"),

    path("business/accounts/myprofile",views.buss_profile, name="buss_profile"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
