from django.urls import path, include
from .views import SeekerProfileAPIView, EducationDetailsAPIView, ExperienceDetailsAPIView, SkillSetAPIView, \
    SeekerSkillsetAPIView, RecommendedJobsAPIView, SearchJobsAPIView

urlpatterns = [
    # profile
    path("profile/", SeekerProfileAPIView.as_view(), name="get_seeker_profile"),
    path("profile/edit/", SeekerProfileAPIView.as_view(), name="edit_seeker_profile"),

    # education
    path("education/all/", EducationDetailsAPIView.as_view(), name="get_seeker_all_educations"),
    path("education/one/<id>/", EducationDetailsAPIView.as_view(), name="get_seeker_one_education"),
    path("education/create/", EducationDetailsAPIView.as_view(), name="create_seeker_education"),
    path("education/<pk>/edit/", EducationDetailsAPIView.as_view(), name="edit_seeker_education"),
    path("education/<pk>/delete/", EducationDetailsAPIView.as_view(), name="delete_seeker_education"),

    # experience
    path("experience/all/", ExperienceDetailsAPIView.as_view(), name="get_all_seeker_experience"),
    path("experience/one/<id>/", ExperienceDetailsAPIView.as_view(), name="get_one_seeker_experience"),
    path("experience/create/", ExperienceDetailsAPIView.as_view(), name="create_seeker_experience"),
    path("experience/<pk>/edit/", ExperienceDetailsAPIView.as_view(), name="edit_seeker_experience"),
    path("experience/<pk>/delete/", ExperienceDetailsAPIView.as_view(), name="delete_seeker_experience"),

    # skillset
    path("skillset/all/", SkillSetAPIView.as_view(), name="get_all_skillsets"),
    path("skillset/one/<id>/", SkillSetAPIView.as_view(), name="get_one_skillset"),

    # seeker skillset
    path("seeker_skillset/", SeekerSkillsetAPIView.as_view(), name="get_seeker_skillset"),
    path("seeker_skillset/create/", SeekerSkillsetAPIView.as_view(), name="create_seeker_skillset"),
    path("seeker_skillset/edit/", SeekerSkillsetAPIView.as_view(), name="edit_seeker_skillset"),
    path("seeker_skillset/delete/", SeekerSkillsetAPIView.as_view(), name="delete_seeker_skillset"),

    # recommended jobs
    path("seeker/recommended-jobs/", RecommendedJobsAPIView.as_view(), name="get_seeker_recommended_jobs"),

    # rearch jobs
    path("seeker/jobs/search/", SearchJobsAPIView.as_view(), name="get_seeker_searched_jobs")
]
