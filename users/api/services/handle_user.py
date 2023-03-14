from django.contrib.auth import get_user_model

from users.models import UserLog


def create_empty_user_log(user_account):
    UserLog.objects.create(user_account=user_account)


def get_user_by_email(email):
    return get_user_model().objects.get(email=email)
