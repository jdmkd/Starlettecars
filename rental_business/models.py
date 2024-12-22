import random
import re
import uuid
from django.utils.safestring import mark_safe
from datetime import date, datetime
from django.utils import timezone
from django.db import models
# from .models import *

# Create your models here.
class business_user(models.Model):
    buss_fname = models.CharField(max_length=20)
    buss_lname = models.CharField(max_length=20)
    buss_emailid = models.CharField(max_length=40)
    buss_password = models.CharField(max_length=30)
    buss_rpassword = models.CharField(max_length=30, blank=True, null=True)
    buss_phonenum = models.CharField(max_length=13, blank=True)
    buss_created_at = models.DateTimeField(default=timezone.now)
    buss_last_login = models.DateTimeField(default=timezone.now)
    
    def update_buss_last_login(self):
        self.buss_last_login = timezone.now()
        self.save()

    buss_auth_token = models.CharField(max_length=100, null=True)
    buss_is_verified = models.BooleanField(default=False)

    buss_updProfile_photo = models.ImageField(
        blank=True, null=True, upload_to="BussProfileImg/"
    )  # , default='profile_img/925667.jpg'

    def buss_updProfile_image(self):
        if self.pk:
            obj = business_user.objects.get(pk=self.pk)
            # print("This is obj ::",obj)
            if obj.buss_updProfile_photo:
                return mark_safe(
                    '<img src="{}" width="100" />'.format(self.buss_updProfile_photo.url)
                )
        else:
            return ""

    buss_updProfile_image.allow_tags = True



    # Identification Details
    buss_date_of_birth = models.DateField(null=True, blank=True)
    buss_aadhaar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    buss_driver_license_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    buss_driver_license_expiry = models.DateField(default=None, null=True, blank=True)
    
    def validate_buss_aadhaar(self):
        """
        Validates the Aadhaar number (India-specific example).
        - Checks if the Aadhaar is 12 digits long.
        - Ensures it contains only numeric characters.
        """
        if not self.buss_aadhaar_number:
            return False, "Aadhaar number is missing."
        
        if len(self.buss_aadhaar_number) != 12:
            return False, "Aadhaar number must be 12 digits long."
        
        if not self.buss_aadhaar_number.isdigit():
            return False, "Aadhaar number must contain only numeric characters."
        
        return True, "Aadhaar number is valid."

    def validate_buss_license(self):
        """
        Validates if the user's driver's license is valid.
        - Ensures the license number is present.
        - Checks if the license expiry date is in the future.
        """
        if not self.buss_driver_license_number:
            return False, "Driver's license number is missing."
        
        if not self.buss_driver_license_expiry:
            return False, "Driver's license expiry date is missing."
        
        if self.buss_driver_license_expiry < date.today():
            return False, "Driver's license has expired."
        
        return True, "Driver's license is valid."
    
    def is_buss_license_valid(self):
        """
        Check if the user's driver's license is still valid.
        """
        from datetime import date
        return self.buss_driver_license_expiry >= date.today()
    
        # pattern = r'^[A-Z]{2}\d{2}[A-Z]{0,2}\d{4}$'
        # return bool(re.match(pattern, license_number))
    
    # Address Details
    buss_address_line1 = models.CharField(max_length=255, null=True, blank=True)
    buss_address_line2 = models.CharField(max_length=255, null=True, blank=True)
    buss_city = models.CharField(max_length=50, null=True, blank=True)
    buss_state = models.CharField(max_length=50, null=True, blank=True)
    buss_zip_code = models.CharField(max_length=10, null=True, blank=True)
    buss_country = models.CharField(max_length=50,null=True, blank=True , default="India")




    buss_role = models.CharField(max_length=30)
    buss_status = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.buss_emailid}'

class buss_vehicle(models.Model):
    buss_vehicle_owner = models.ForeignKey(business_user, on_delete=models.CASCADE, null=True)
    buss_vehicle_id = models.CharField(max_length=10, default='BUS1000')
    VEHICLE_COMPANY_CHOICES = (
        ('Toyota', 'Toyota'),
        ('Mahindra','Mahindra'),
        ('Honda', 'Honda'),
        ('Ford', 'Ford'),
        ('Chevrolet', 'Chevrolet'),
        ('Tata Motors', 'Tata Motors'),
        ('Nissan', 'Nissan'),
        ('Volkswagen', 'Volkswagen'),
        ('BMW', 'BMW'),
        ('Mercedes-Benz', 'Mercedes-Benz'),
        ('Audi', 'Audi'),
        ('Hyundai', 'Hyundai'),
        ('Suzuki', "Suzuki"),
        ('Kia', 'Kia'),
        ('Subaru', 'Subaru'),
        ('Mazda', 'Mazda'),
        ('Lexus', 'Lexus'),
        ('Jeep', 'Jeep'),
        ('Chrysler', 'Chrysler'),
        ('Volvo', 'Volvo'),
        ('Porsche', 'Porsche'),
        ('Land Rover', 'Land Rover'),
        ('Tesla', 'Tesla'),
        ('MG Motors','MG Motors'),
        # Add more options as needed
    )
    buss_vehicle_company_name = models.CharField(max_length=40, choices=VEHICLE_COMPANY_CHOICES)
    buss_vehicle_model = models.CharField(max_length=50, null=True)
    # buss_vehicle_year = models.PositiveIntegerField()

    VEHICLE_COLOR_CHOICES = (
        ('Black', 'Black'),
        ('White', 'White'),
        ('Silver', 'Silver'),
        ('Gray', 'Gray'),
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Yellow', 'Yellow'),
        ('Orange', 'Orange'),
        ('Purple', 'Purple'),
        ('Brown', 'Brown'),
        ('Beige', 'Beige'),
        ('Gold', 'Gold'),
        ('Other', 'Other'),
    )
    buss_vehicle_color = models.CharField(max_length=20, choices=VEHICLE_COLOR_CHOICES)
    buss_vehicle_number = models.CharField(max_length=40)

    CAR_TYPE_CHOICES = (
        ('SUV', 'SUV (Sports Utility Vehicle)'),
        ('Sedan', 'Sedan'),
        ('Hatchback', 'Hatchback'),
        ('Convertible', 'Convertible'),
        ('Truck', 'Truck'),
        ('Van', 'Van'),
        ('Coupe', 'Coupe'),
        ('Crossover', 'Crossover'),
        ('Minivan', 'Minivan'),
        ('Pickup', 'Pickup Truck'),
        ('Wagon', 'Wagon'),
        ('Electric', 'Electric Car'),
        ('Luxury', 'Luxury Car'),
        ('Sports', 'Sports Car'),
        ('Hybrid', 'Hybrid Car'),
        ('Station_Wagon', 'Station Wagon'),
        ('Compact', 'Compact Car'),
        ('Muscle', 'Muscle Car'),
        ('Supercar', 'Supercar'),
        ('Classic', 'Classic Car'),
        ('Off_Road', 'Off-Road Vehicle'),
        ('Roadster', 'Roadster'),
        ('Limousine', 'Limousine'),
        ('Microcar', 'Microcar'),
        ('Subcompact', 'Subcompact Car'),

            # Add more options as needed
        )
    buss_vehicle_type = models.CharField(max_length=40, choices=CAR_TYPE_CHOICES)

    def validate_chassis_number(chassis_number):
        pattern = r'^[A-HJ-NPR-Z0-9]{17}$'
        return re.match(pattern, chassis_number) is not None
    # print(validate_chassis_number("1HGCM82633A123456"))  # Output: True
    # print(validate_chassis_number("INVALID-CHASSIS"))    # Output: False
    
    buss_chassi_number = models.CharField(max_length=17, unique=True, null=True, validators=[validate_chassis_number],)

    buss_year_of_manufacture = models.PositiveIntegerField(null=True)

    buss_registration_date = models.DateField(blank=True, null=True)





    buss_vehicle_location = models.CharField(blank=True, null=True, max_length=20)
    buss_rent_per_day = models.CharField(max_length=40)
    
    buss_vehicle_description = models.TextField()    
    buss_vehicle_is_verified = models.BooleanField(default=False)
    buss_vehicle_is_soldout = models.BooleanField(default=False)

    VEHICLE_STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Booked', 'Booked'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Out of Service', 'Out of Service'),
    )
    buss_vehicle_status = models.CharField(max_length=20, choices=VEHICLE_STATUS_CHOICES)

    

    # buss_vehicle_auth_token = models.CharField(max_length=100, null=True)
    # vin = models.CharField(max_length=17) #VIN (Vehicle Identification Number
    # fuel_type = models.CharField(max_length=20)
    # transmission = models.CharField(max_length=20)
    # seating_capacity = models.PositiveIntegerField()
    # doors = models.PositiveIntegerField()
    # engine_displacement = models.FloatField()
    # fuel_efficiency = models.CharField(max_length=20)
    # fuel_type = models.CharField(max_length=20)
    # transmission = models.CharField(max_length=20)
    # seating_capacity = models.PositiveIntegerField()
    # doors = models.PositiveIntegerField()
    # engine_displacement = models.FloatField()
    # fuel_efficiency = models.CharField(max_length=20)
    # customer_reviews = models.JSONField()  # Use JSONField or related for structured reviews
    # payment_information = models.TextField()  # Same as features, consider using a structured field
    # discounts_promotions = models.TextField()  # Same as features, consider using a structured field
    # min_age = models.PositiveIntegerField()
    # max_age = models.PositiveIntegerField()
    # terms_conditions = models.TextField()
    # booking_system = models.CharField(max_length=50)
    # pickup_dropoff_instructions = models.TextField()
    buss_vehicle_photo = models.ImageField(upload_to="rental_buss/added_vehicles/")
    def buss_vehicle_image(self):
        if self.pk:
            obj = buss_vehicle.objects.get(pk=self.pk)
            # print("This is obj ::",obj)
            if obj.buss_vehicle_photo:
                return mark_safe('<img src="{}" width="100" />'.format(self.buss_vehicle_photo.url))

    buss_vehicle_image.allow_tags = True

    def __str__(self):
        return f'{self.buss_vehicle_id} {self.buss_vehicle_owner}'
    

class buss_feedback(models.Model):
    buss_l_id = models.ForeignKey(business_user, on_delete=models.CASCADE)
    buss_name = models.CharField(max_length=30)
    buss_ratings = models.CharField(max_length=25)
    buss_comments = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.buss_name}'


class buss_contactus(models.Model):
    buss_name = models.CharField(max_length=30)
    buss_email = models.CharField(max_length=30)
    buss_phone = models.CharField(max_length=30)
    buss_message = models.CharField(max_length=30)
    buss_contact_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.buss_name}'