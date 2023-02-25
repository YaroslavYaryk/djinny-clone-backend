from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions
from rest_framework.fields import SerializerMethodField

from users.models import UserLog, UserType


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    user_type_id = serializers.IntegerField()

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "user_type_id")
        write_only_fields = "password"
        read_only_fields = (
            "registration_date",
            "staff",
            "admin",
        )

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = "__all__"
        write_only_fields = "password"
        read_only_fields = (
            "registration_date",
            "staff",
            "admin",
        )


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ("last_login", "registration_date", "staff", "admin", "password")


class UserLogSerializer(serializers.ModelSerializer):
    last_login = SerializerMethodField()

    class Meta:
        model = UserLog
        fields = "__all__"

    def get_last_login(self, instance: UserLog):
        print("here")
        return instance.user_account.last_login


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = "__all__"


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = ('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = ('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = ('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        data['user'] = user
        return data
