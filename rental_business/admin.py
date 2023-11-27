from django.contrib import admin
from .models import business_user, buss_vehicle, buss_contactus, buss_feedback


# Register your models here.
class show_business_user(admin.ModelAdmin):
    list_display = [
        "id",
        "buss_fname",
        "buss_lname",
        "buss_emailid",
        "buss_phonenum",
        "buss_updProfile_image",
        "buss_updProfile_photo",
        "buss_password",
        "buss_rpassword",
        "buss_created_at",
        "buss_last_login",
        "buss_auth_token",
        "buss_role",
        "buss_status",
        "buss_is_verified",
    ]
admin.site.register(business_user, show_business_user)


class show_buss_vehicle(admin.ModelAdmin):
    list_display = [
        "id",
        "buss_vehicle_id",
        "buss_vehicle_owner",
        "buss_vehicle_company_name",
        "buss_vehicle_model",
        "buss_vehicle_color",
        "buss_vehicle_number",
        "buss_vehicle_type",
        "buss_vehicle_photo",
        "buss_vehicle_image",
        "buss_vehicle_description",
        "buss_rent_per_day",
        "buss_vehicle_location",
        "buss_vehicle_is_verified",
        "buss_vehicle_is_soldout",
        "buss_vehicle_status",
    ]
admin.site.register(buss_vehicle, show_buss_vehicle)


class show_buss_contactus(admin.ModelAdmin):
    list_display = ["buss_name", "buss_email", "buss_phone", "buss_message", "buss_contact_date"]
admin.site.register(buss_contactus, show_buss_contactus)


class show_buss_feedback(admin.ModelAdmin):
    list_display = ["buss_l_id", "buss_name", "buss_ratings", "buss_comments"]
admin.site.register(buss_feedback, show_buss_feedback)

