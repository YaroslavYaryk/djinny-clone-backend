from django.shortcuts import get_object_or_404
from seeker.models import ExperienceDetails
from .handle_seeker_profile import get_seeker_profile_by_user_account


def get_one_experience_for_user(user, pk):
    seeker_profile = get_seeker_profile_by_user_account(user)
    return get_object_or_404(ExperienceDetails, profile_account=seeker_profile, pk=pk)


def get_experience_for_user(user):
    seeker_profile = get_seeker_profile_by_user_account(user)
    return ExperienceDetails.objects.filter(profile_account=seeker_profile)


def get_experience_by_id(pk):
    return get_object_or_404(ExperienceDetails, pk=pk)


def delete_experience(pk):
    education = get_experience_by_id(pk)
    education.delete()
