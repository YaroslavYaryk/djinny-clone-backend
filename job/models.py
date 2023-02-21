from django.db import models
from users.models import User
from company.models import Company
from seeker.models import SkillSet


# Create your models here.
class JobPost(models.Model):
    posted_by = models.ForeignKey(User, verbose_name="Account", on_delete=models.CASCADE)
    job_type = models.ForeignKey("JobType", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name="Company", on_delete=models.CASCADE)
    is_company_name_hidden = models.BooleanField(default=False)
    created_date = models.DateField(auto_now=True)
    job_description = models.TextField(max_length=500)
    job_location = models.ForeignKey("JobLocation", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class JobType(models.Model):
    job_type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.job_type}"


class JobPostActivity(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    apply_date = models.DateField(auto_now=True)
    edited_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"job - {self.job_post}, apply date - {self.apply_date}"


class JobPostSkillSet(models.Model):
    skill_set = models.ForeignKey(SkillSet, on_delete=models.CASCADE, related_name="job_skill_set")
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="job_post_skill")
    skill_level = models.IntegerField()

    class Meta:
        unique_together = ["skill_set", "job_post"]

    def __str__(self):
        return f"job - {self.job_post},  skill set - {self.skill_set}"


class JobLocation(models.Model):
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)

    def __str__(self):
        return f"city - {self.city}, country - {self.country}"
