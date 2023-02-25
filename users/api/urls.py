from django.urls import re_path, path
from rest_framework.authtoken.views import obtain_auth_token
from .views import CreateUserAPIView, LogoutUserAPIView, UserApiView, CustomObtainAuthToken, UserLogAPIView, \
    UserTypeAPIView

urlpatterns = [
    re_path(r"^auth/login/$", CustomObtainAuthToken.as_view(), name="auth_user_login"),
    re_path(r"^auth/register/$", CreateUserAPIView.as_view(), name="auth_user_create"),
    re_path(r"^auth/logout/$", LogoutUserAPIView.as_view(), name="auth_user_logout"),
    path("profile/", UserApiView.as_view(), name="user_profile"),
    path("profile/edit/", UserApiView.as_view(), name="user_profile"),
    path("log/", UserLogAPIView.as_view(), name="user_log"),
    path("types/", UserTypeAPIView.as_view(), name="get_all_user_types"),

]
