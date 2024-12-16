# Generated by Django 5.0.6 on 2024-11-18 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0012_alter_usertable_auth_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertable',
            name='aadhaar_number',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='usertable',
            name='address_line1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='usertable',
            name='address_line2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='usertable',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usertable',
            name='country',
            field=models.CharField(blank=True, default='India', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usertable',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usertable',
            name='driver_license_expiry',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usertable',
            name='driver_license_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='usertable',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usertable',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]