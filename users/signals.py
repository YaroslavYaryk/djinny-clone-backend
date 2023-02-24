from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from users.models import User, UserType
from seeker.models import SeekerProfile
from seeker.api.services import handle_seeker_profile
from users.api.services import handle_user


@receiver(post_save, sender=User)
def create(sender, instance: User, created, **kwargs):
    if created and instance.user_type.has_additional_profile:
        handle_seeker_profile.create_empty_seeker_profile(user_account=instance)


@receiver(post_save, sender=User)
def create_user_log(sender, instance: User, created, **kwargs):
    if created:
        handle_user.create_empty_user_log(instance)
