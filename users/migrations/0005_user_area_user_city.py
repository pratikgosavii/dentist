# Generated by Django 5.1.4 on 2025-05-15 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0010_alter_enquiry_enquiry_type'),
        ('users', '0004_remove_user_is_daycare_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.area'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.city'),
        ),
    ]
