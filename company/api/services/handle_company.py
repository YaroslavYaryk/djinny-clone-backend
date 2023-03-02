from django.http import Http404
from django.shortcuts import get_object_or_404

from company.models import Company, CompanyImage, BusinessStream


def handle_user_access_to_company(company, user):
    return company.user_account == user


def get_company_by_id(pk):
    return get_object_or_404(Company, pk=pk)


def get_company_by_for_user_by_id(pk, user):
    return get_object_or_404(Company, pk=pk, user_account=user)


def get_companies_for_user(user):
    return Company.objects.filter(user_account=user)


def delete_company(pk, user):
    get_company_by_for_user_by_id(pk, user).delete()


def get_images_for_company(company_id):
    return CompanyImage.objects.filter(company__id=company_id)


def get_parsed_images(data: dict):
    return (value for key, value in data.items() if key[:5] == "image")


def get_company_image_by_id(image_id):
    return CompanyImage.objects.get(pk=image_id)


def create_company_image(company_id, image):
    CompanyImage.objects.create(company_id=company_id, company_image=image)


def add_company_images(company_id, data):
    for image in data:
        create_company_image(company_id, image)


def delete_company_image(image_id):
    get_company_image_by_id(image_id).delete()


def delete_all_images(company_id):
    get_images_for_company(company_id).delete()


def get_business_stream_queryset():
    return BusinessStream.objects.all()


def get_jobs_for_company(company_id):
    company = get_company_by_id(company_id)
    return company.company_jobs.all()
