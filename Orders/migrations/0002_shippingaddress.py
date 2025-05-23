# Generated by Django 5.2 on 2025-05-06 12:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=255, verbose_name='Address line 1')),
                ('address_line2', models.CharField(blank=True, max_length=255, verbose_name='Address line 2')),
                ('city', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20, verbose_name='Postal / ZIP code')),
                ('country', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=30)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='Orders.order')),
            ],
        ),
    ]
