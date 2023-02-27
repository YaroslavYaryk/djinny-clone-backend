from django.urls import path, include
from .views import JobTypeAPIView, JobPostAPIView, JobActivityAPIView, JobLocationAPIView

urlpatterns = [
    # job type
    path("job-type/all/", JobTypeAPIView.as_view(), name="get_all_job_types"),
    path("job-type/one/<id>/", JobTypeAPIView.as_view(), name="get_one_job_type"),

    # job post
    path("job-post/all/", JobPostAPIView.as_view(), name="get_all_job_posts"),
    path("job-post/one/<id>/", JobPostAPIView.as_view(), name="get_one_job_post"),
    path("job-post/create/", JobPostAPIView.as_view(), name="create_one_job_post"),
    path("job-post/<pk>/edit/", JobPostAPIView.as_view(), name="edit_one_job_post"),
    path("job-post/<pk>/delete/", JobPostAPIView.as_view(), name="delete_one_job_post"),

    # job activity
    path("job-post/<pk>/activity/", JobActivityAPIView.as_view(), name="get_job_activity"),

    # job location
    path("job-post/<id>/location/all/", JobLocationAPIView.as_view(), name="get_all_job_location"),
    path("job-post/<id>/location/one/<location_id>/", JobLocationAPIView.as_view(), name="get_one_job_location"),
    path("job-post/<pk>/location/create/", JobLocationAPIView.as_view(), name="create_job_location"),
    path("job-post/<pk>/location/<location_id>/edit/", JobLocationAPIView.as_view(), name="edit_job_location"),
    path("job-post/<pk>/location/<location_id>/delete/", JobLocationAPIView.as_view(), name="delete_job_location"),

]
