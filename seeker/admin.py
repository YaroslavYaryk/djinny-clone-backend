from django.contrib import admin
from .models import SeekerProfile, SkillSet, SeekerSkillSet, ExperienceDetails, EducationDetail

# Register your models here.
admin.site.register(SeekerProfile)
admin.site.register(SkillSet)
admin.site.register(SeekerSkillSet)
admin.site.register(ExperienceDetails)
admin.site.register(EducationDetail)
