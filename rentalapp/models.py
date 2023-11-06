from django.utils.safestring import mark_safe
from django.utils import timezone
import uuid
from django.db import models
from rental_business.models import buss_vehicle
# Create your models here.


class usertable(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    emailid = models.CharField(max_length=40)
    password = models.CharField(max_length=30)
    rpassword = models.CharField(max_length=30, blank=True, null=True)
    phonenum = models.CharField(max_length=13, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    auth_token = models.CharField(max_length=100, null=True)
    
    password_reset_token = models.CharField(max_length=100, null=True)
    password_reset_token_expiration_time = models.DateTimeField(null=True)
    def is_password_reset_token_expired(self):
        return timezone.now() > self.password_reset_token_expiration_time
    
    is_verified = models.BooleanField(default=False)

    # licence_no = models.CharField(max_length=50)
    # address = models.TextField()
    updProfile_photo = models.ImageField(
        blank=True, null=True, upload_to="UserProfileImg/"
    )  # , default='profile_img/925667.jpg'

    def updProfile_image(self):
        if self.pk:
            obj = usertable.objects.get(pk=self.pk)
            # print("This is obj ::",obj)
            if obj.updProfile_photo:
                return mark_safe(
                    '<img src="{}" width="100" />'.format(self.updProfile_photo.url)
                )
        else:
            return ""

    updProfile_image.allow_tags = True

    role = models.CharField(max_length=30)
    status = models.CharField(max_length=30)

    def __str__(self):
        return self.emailid
        return self.fname


# class vehicle_table(models.Model):
#     vehicle_name = models.CharField(max_length=40)
#     vehicle_color = models.CharField(max_length=40)
#     vehicle_number = models.CharField(max_length=40)
#     vehicle_type = models.CharField(max_length=40)
#     vehicle_location = models.CharField(default="None", max_length=20)
#     rent_per_day = models.CharField(max_length=40)
#     vehicle_photo = models.ImageField(upload_to="photos")
#     vehicle_description = models.TextField()

#     def vehicle_image(self):
#         return mark_safe('<img src="{}" width="100" />'.format(self.vehicle_photo.url))

#     vehicle_image.allow_tags = True

#     def __str__(self):
#         return self.vehicle_name



class booking_table(models.Model):
    vehicle_id = models.ForeignKey(buss_vehicle, on_delete=models.CASCADE)
    # vehicle_table
    login_id = models.ForeignKey(usertable, on_delete=models.CASCADE)
    from_duration = models.DateField(blank=False, null=False)
    from_to = models.DateField(blank=False, null=False)
    amount = models.CharField(max_length=30)
    booking_date = models.DateTimeField(auto_now_add=True)
    paystatus = models.BooleanField(default=False)
    
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    def __int__(self):
        self.vehicle_id
        self.booking_date


class feedback(models.Model):
    l_id = models.ForeignKey(usertable, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    ratings = models.CharField(max_length=25)
    comments = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class contactus(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    message = models.CharField(max_length=30)
    contact_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name
