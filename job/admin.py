from django.contrib import admin

from .models import JobType, JobPost, JobLocation, JobPostActivity, JobPostSkillSet, JobConversation, \
    ConversationMessage

# Register your models here.

admin.site.register(JobPost)
admin.site.register(JobType)
admin.site.register(JobLocation)
admin.site.register(JobPostActivity)
admin.site.register(JobPostSkillSet)
admin.site.register(JobConversation)
admin.site.register(ConversationMessage)
