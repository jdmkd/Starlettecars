# Generated by Django 5.0.6 on 2024-11-17 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0011_feedback_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertable',
            name='auth_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usertable',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usertable',
            name='password_reset_token_expiration_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usertable',
            name='phonenum',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]