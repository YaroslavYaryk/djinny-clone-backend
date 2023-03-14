from django.urls import path, include
from .views import CompanyAPIView, CompanyImagesAPIView, delete_all_company_images, BusinessStreamStreamAPIView, \
    CompanyJobAPIView

urlpatterns = [
    # company
    path("companies/all/", CompanyAPIView.as_view(), name="get_all_companies"),
    path("companies/one/<id>/", CompanyAPIView.as_view(), name="get_one_company"),
    path("companies/create/", CompanyAPIView.as_view(), name="create_company"),
    path("companies/<pk>/edit/", CompanyAPIView.as_view(), name="edit_company"),
    path("companies/<pk>/delete/", CompanyAPIView.as_view(), name="delete_company"),

    # company images
    path("company/<pk>/images/", CompanyImagesAPIView.as_view(), name="get_company_images"),
    path("company/<pk>/images/add/", CompanyImagesAPIView.as_view(), name="add_company_images"),
    path("company/<pk>/images/<image_id>/delete/", CompanyImagesAPIView.as_view(), name="delete_company_image"),
    path("company/<pk>/images/delete-all/", delete_all_company_images, name="delete_all_company_images"),

    #  business stream
    path("business-stream/all/", BusinessStreamStreamAPIView.as_view(), name="get_all_business_streams"),

    # company jobs
    path("company/<pk>/jobs/", CompanyJobAPIView.as_view(), name="get_jobs_for_company")

]
