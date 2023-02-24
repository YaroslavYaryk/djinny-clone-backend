from django.db import models
from users.models import User


# Create your models here.
class SeekerProfile(models.Model):
    user_account = models.ForeignKey(User, verbose_name="Account", on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name="First name", max_length=255, null=True)
    last_name = models.CharField(verbose_name="Last name", max_length=255, null=True)
    current_salary = models.IntegerField(null=True)
    is_annually_monthly = models.BooleanField(default=True)
    currency = models.CharField(max_length=50, verbose_name="Currency", null=True)

    def __str__(self):
        return f"account - {self.user_account}"


class EducationDetail(models.Model):
    profile_account = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE, related_name="seeker_educations")
    certificate_degree_name = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    institute_university_name = models.CharField(max_length=50)
    starting_date = models.DateField()
    completion_date = models.DateField()
    percentage = models.FloatField()
    cgpa = models.FloatField()

    class Meta:
        unique_together = ["profile_account", "certificate_degree_name", "major"]

    def __str__(self):
        return f"account - {self.profile_account}, certificate degree - {self.certificate_degree_name}"


class ExperienceDetails(models.Model):
    profile_account = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE, related_name="seeker_experiences")
    is_current_job = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
    job_title = models.CharField(max_length=50, verbose_name="Job title")
    company_name = models.CharField(max_length=50, verbose_name="Company name")
    job_location_city = models.CharField(max_length=50, verbose_name="City")
    job_location_state = models.CharField(max_length=50, verbose_name="state")
    job_location_country = models.CharField(max_length=50, verbose_name="country")
    description = models.TextField(max_length=4000)

    class Meta:
        unique_together = ["profile_account", "start_date", "end_date"]

    def __str__(self):
        return f"account - {self.profile_account}, start date - {self.start_date}, end date - {self.end_date}"


class SkillSet(models.Model):
    name = models.CharField(max_length=50, verbose_name="skill set name")

    def __str__(self):
        return f"name - {self.name}"


class SeekerSkillSet(models.Model):
    profile_account = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE, related_name="seeker_skill_set")
    skill_set = models.ForeignKey(SkillSet, on_delete=models.CASCADE)
    skill_level = models.IntegerField()

    class Meta:
        unique_together = ["profile_account", "skill_set"]

    def __str__(self):
        return f"account - {self.profile_account}, skill-set - {self.skill_set.name}"
