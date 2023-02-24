from seeker.models import SeekerProfile


def create_empty_seeker_profile(user_account):
    SeekerProfile.objects.create(user_account=user_account)
