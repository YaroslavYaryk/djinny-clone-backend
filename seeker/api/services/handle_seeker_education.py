from django.shortcuts import get_object_or_404

from seeker.models import EducationDetail
from .handle_seeker_profile import get_seeker_profile_by_user_account


def get_educations_for_user(user):
    seeker_profile = get_seeker_profile_by_user_account(user)
    return EducationDetail.objects.filter(profile_account=seeker_profile)


def get_one_education_for_user(user, pk):
    seeker_profile = get_seeker_profile_by_user_account(user)
    return get_object_or_404(EducationDetail, profile_account=seeker_profile, pk=pk)


def get_education_by_id(pk):
    return get_object_or_404(EducationDetail, pk=pk)


def delete_education(pk):
    education = get_education_by_id(pk)
    education.delete()
