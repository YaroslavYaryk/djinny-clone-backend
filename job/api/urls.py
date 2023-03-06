from django.urls import path, include
from .views import JobTypeAPIView, JobPostAPIView, JobActivityAPIView, JobLocationAPIView, JobSkillSetAPIView, \
    JobConversationAPIView, ConversationMessageAPIView

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

    # job skillset
    path("job-post/<pk>/skillset/", JobSkillSetAPIView.as_view(), name="get_all_job_skillset"),
    path("job-post/<pk>/skillset/create/", JobSkillSetAPIView.as_view(), name="create_job_skillset"),
    path("job-post/<pk>/skillset/edit/", JobSkillSetAPIView.as_view(), name="edit_job_skillset"),
    path("job-post/<pk>/skillset/delete/", JobSkillSetAPIView.as_view(), name="delete_job_skillset"),

    # conversation
    path("conversation/all/", JobConversationAPIView.as_view(), name="get_all_conversations"),
    path("conversation/one/<id>/", JobConversationAPIView.as_view(), name="get_one_conversations"),
    path("conversation/job/<job_id>/create/<user_type>/<user_id>/", JobConversationAPIView.as_view(),
         name="create_one_conversations"),
    path("conversation/one/<conversation_id>/delete/", JobConversationAPIView.as_view(),
         name="delete_one_conversations"),

    # conversation message
    path("conversation/<pk>/messages/all/", ConversationMessageAPIView.as_view(),
         name="get_all_messages_for_conversation"),
    path("conversation/<pk>/messages/one/<message_id>/", ConversationMessageAPIView.as_view(),
         name="get_one_message_for_conversation"),
    path("conversation/<pk>/messages/create/", ConversationMessageAPIView.as_view(),
         name="add_message_to_conversation"),
    path("conversation/<pk>/messages/<message_id>/edit/", ConversationMessageAPIView.as_view(),
         name="edit_message_to_conversation"),
    path("conversation/<pk>/messages/<message_id>/delete/", ConversationMessageAPIView.as_view(),
         name="delete_message_to_conversation"),

]
