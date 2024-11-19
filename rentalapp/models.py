from datetime import date
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
    phonenum = models.CharField(max_length=13, blank=True,  null=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    
    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()

    date_of_birth = models.DateField(null=True, blank=True)
    
    # Identification Details
    aadhaar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    driver_license_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    driver_license_expiry = models.DateField(default=None, null=True, blank=True)
    def validate_aadhaar(self):
        """
        Validates the Aadhaar number (India-specific example).
        - Checks if the Aadhaar is 12 digits long.
        - Ensures it contains only numeric characters.
        """
        if not self.aadhaar_number:
            return False, "Aadhaar number is missing."
        
        if len(self.aadhaar_number) != 12:
            return False, "Aadhaar number must be 12 digits long."
        
        if not self.aadhaar_number.isdigit():
            return False, "Aadhaar number must contain only numeric characters."
        
        return True, "Aadhaar number is valid."

    def validate_license(self):
        """
        Validates if the user's driver's license is valid.
        - Ensures the license number is present.
        - Checks if the license expiry date is in the future.
        """
        if not self.driver_license_number:
            return False, "Driver's license number is missing."
        
        if not self.driver_license_expiry:
            return False, "Driver's license expiry date is missing."
        
        if self.driver_license_expiry < date.today():
            return False, "Driver's license has expired."
        
        return True, "Driver's license is valid."
    
    def is_license_valid(self):
        """
        Check if the user's driver's license is still valid.
        """
        from datetime import date
        return self.driver_license_expiry >= date.today()
    
    # Address Details
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50,null=True, blank=True , default="India")


    

    auth_token = models.CharField(max_length=100, blank=True, null=True)
    
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_token_expiration_time = models.DateTimeField(null=True, blank=True)
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
        return f'{self.emailid}'


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
        return f'{self.vehicle_id} {self.booking_date}'


class feedback(models.Model):
    l_id = models.ForeignKey(usertable, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, null=True)
    ratings = models.CharField(max_length=25)
    comments = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class contactus(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    message = models.CharField(max_length=30)
    contact_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.name}'
