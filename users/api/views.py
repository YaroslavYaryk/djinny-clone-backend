from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CreateUserSerializer, UserSerializer, CustomAuthTokenSerializer, UserEditSerializer, \
    UserLogSerializer, UserTypeSerializer
from django.db.utils import IntegrityError
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import update_last_login
from users.models import UserType


@api_view(('GET',))
def index(request):
    return Response({})


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            update_last_login(None, user)
            headers = self.get_success_headers(serializer.data)
            # We create a token than will be used for future auth
            token = Token.objects.create(user=serializer.instance)
            token_data = {"token": token.key}
            return Response(
                {**serializer.data, **token_data},
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except IntegrityError as err:
            raise err
            return Response({"message": str(err)}, status.HTTP_401_UNAUTHORIZED)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=result.data['token'])
        update_last_login(None, token.user)
        return result


class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserEditSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_403_FORBIDDEN)


class UserLogAPIView(APIView):
    def get(self, request):
        instance = request.user.user_account_log
        serializer = UserLogSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTypeAPIView(APIView):
    def get(self, request):
        queryset = UserType.objects.all()
        serializer = UserTypeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
