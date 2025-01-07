# hospital_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Admin, CustomUser  

@receiver(post_save, sender=CustomUser)
def create_admin_entry(sender, instance, created, **kwargs):
    if created and instance.is_staff:  # Check if it's an admin user
        Admin.objects.create(user=instance)  # Create corresponding Admin entry
