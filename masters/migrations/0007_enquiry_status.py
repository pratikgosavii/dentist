# Generated by Django 5.1.4 on 2025-05-13 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0006_city_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('completed', 'Completed')], default='Pending', max_length=10),
        ),
    ]
