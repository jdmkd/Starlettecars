from django.contrib import admin
from .models import usertable, booking_table, feedback, contactus
from rental_business.models import buss_vehicle
# Register your models here.


class showuser(admin.ModelAdmin):
    list_display = [
        "id",
        "fname",
        "lname",
        "emailid",
        "phonenum",
        "updProfile_image",
        "updProfile_photo",
        "password",
        "created_at",
        "last_login",
        "date_of_birth",
        "aadhaar_number",
        "driver_license_number",
        "driver_license_expiry",
        "address_line1",
        "address_line2",
        "city",
        "state",
        "zip_code",
        "country",
        "auth_token",
        "password_reset_token",
        "password_reset_token_expiration_time",
        "role",
        "status",
        "is_verified",
    ]


admin.site.register(usertable, showuser)


# class showvehicle(admin.ModelAdmin):
#     list_display = [
#         "id",
#         "vehicle_name",
#         "vehicle_color",
#         "vehicle_number",
#         "vehicle_type",
#         "vehicle_image",
#         "vehicle_description",
#         "rent_per_day",
#         "vehicle_location",
#     ]


# admin.site.register(vehicle_table, showvehicle)


class showbookings(admin.ModelAdmin):
    list_display = [
        "id",
        "login_id",
        "vehicle_id",
        "get_vehicle_model",
        "get_vehicle_status",
        "is_cancelled",
        "cancelled_at",
        "booking_date",
        "from_duration",
        "from_to",
        "amount",
        "paystatus",
    ]

    def get_vehicle_status(self, id):
        return id.vehicle_id.buss_vehicle_status if id.vehicle_id else None
    get_vehicle_status.buss_vehicle_status = 'Vehicle Name'

    def get_vehicle_model(self, id):
        return id.vehicle_id.buss_vehicle_model if id.vehicle_id else None
    get_vehicle_model.buss_vehicle_model = 'Vehicle Name'
admin.site.register(booking_table, showbookings)


class showfeedback(admin.ModelAdmin):
    list_display = ["id","email", "name", "ratings", "comments"]
admin.site.register(feedback, showfeedback)


class showcontactus(admin.ModelAdmin):
    list_display = ["id","name", "email", "phone", "message", "contact_date"]
admin.site.register(contactus, showcontactus)
