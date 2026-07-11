from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        from account.models import Profile
        Profile.objects.create(user=instance)
        print(f"Profile created for {instance.full_name}")