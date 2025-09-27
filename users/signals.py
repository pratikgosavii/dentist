from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from doctor.models import Tooth
from .models import User


# Tooth numbers for 32 teeth (exclude wisdom teeth)

TOOTH_NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', 
 '9', '10', '11', '12', '13', '14', '15', '16',
 '17', '18', '19', '20', '21', '22', '23', '24',
 '25', '26', '27', '28', '29', '30', '31', '32']


@receiver(post_save, sender=User)
def create_teeth_for_customer(sender, instance, created, **kwargs):
    if (created and instance.is_customer) or (
        not created and instance.is_customer and not instance.teeth.exists()
    ):
        Tooth.objects.bulk_create([
            Tooth(user=instance, number=tn) for tn in TOOTH_NUMBERS
        ])
