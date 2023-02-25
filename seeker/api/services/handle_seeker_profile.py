from seeker.models import SeekerProfile


def create_empty_seeker_profile(user_account):
    SeekerProfile.objects.create(user_account=user_account)


def get_seeker_profile_by_user_account(user):
    try:
        return SeekerProfile.objects.get(user_account=user)
    except Exception as ex:
        return None
