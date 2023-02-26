from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions
from rest_framework.fields import SerializerMethodField
from company.models import Company, CompanyImage, BusinessStream


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CompanyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyImage
        fields = "__all__"


class BusinessStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessStream
        fields = "__all__"
