import datetime

from dateutil.relativedelta import relativedelta

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


def handle_dates_difference_in_years(start_date, end_date):
    return round(relativedelta(end_date, start_date).months / 12, 1)


def end_date_for_seeker_experience(experience):
    if not experience.is_current_job:
        return experience.end_date
    return datetime.date.today()


def get_seeker_experience_years(user):
    experiences = get_experience_for_user(user)
    if not experiences:
        return 0
    years_in_total = 0
    for experience in experiences:
        start_date = experience.start_date
        end_date = end_date_for_seeker_experience(experience)
        years_in_total += handle_dates_difference_in_years(start_date, end_date)

    return years_in_total
