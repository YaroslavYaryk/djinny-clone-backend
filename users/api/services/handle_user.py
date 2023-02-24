from users.models import UserLog


def create_empty_user_log(user_account):
    UserLog.objects.create(user_account=user_account)
