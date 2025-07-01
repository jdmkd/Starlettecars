from django import forms
from .models import buss_vehicle

class BussVehicleForm(forms.ModelForm):
    class Meta:
        model = buss_vehicle
        fields = [
            'buss_vehicle_company_name',
            'buss_vehicle_model',
            'buss_vehicle_type',
            'buss_vehicle_color',
            'buss_vehicle_status',
            'buss_vehicle_number',
            'buss_chassi_number',
            'buss_year_of_manufacture',
            'buss_registration_date',
            'buss_vehicle_location',
            'buss_rent_per_day',
            'buss_vehicle_description',
            'buss_vehicle_photo',
        ]
        widgets = {
            'buss_registration_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_classes = {
            'buss_vehicle_company_name': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_vehicle_model': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_vehicle_type': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_vehicle_color': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_vehicle_status': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_vehicle_number': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_chassi_number': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_year_of_manufacture': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_registration_date': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_vehicle_location': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_rent_per_day': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_vehicle_description': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
            'buss_vehicle_photo': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-xl md:text-2xl normal-case',
        }
        for field_name, css_class in field_classes.items():
            if field_name in self.fields:
                existing = self.fields[field_name].widget.attrs.get('class', '')
                self.fields[field_name].widget.attrs['class'] = f"{existing} {css_class}".strip()
        # Add placeholders and other attributes as needed
        self.fields['buss_vehicle_model'].widget.attrs['placeholder'] = 'e.g., Fortuner, Creta, Swift'
        self.fields['buss_vehicle_number'].widget.attrs['placeholder'] = 'e.g., MH12AB1234'
        self.fields['buss_chassi_number'].widget.attrs['placeholder'] = '17-character VIN'
        self.fields['buss_year_of_manufacture'].widget.attrs['placeholder'] = 'e.g., 2020'
        self.fields['buss_year_of_manufacture'].widget.attrs['min'] = '1900'
        self.fields['buss_year_of_manufacture'].widget.attrs['max'] = '2030'
        self.fields['buss_vehicle_location'].widget.attrs['placeholder'] = 'e.g., Mumbai, Delhi'
        self.fields['buss_rent_per_day'].widget.attrs['placeholder'] = 'e.g., 1500'
        self.fields['buss_rent_per_day'].widget.attrs['min'] = '0'
        self.fields['buss_vehicle_description'].widget.attrs['placeholder'] = 'Describe your vehicle features, condition, etc.' 