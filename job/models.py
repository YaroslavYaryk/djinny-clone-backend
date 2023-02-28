from django.db import models
from users.models import User
from company.models import Company
from seeker.models import SkillSet, SeekerProfile


# Create your models here.
class JobPost(models.Model):
    posted_by = models.ForeignKey(User, verbose_name="Account", on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50, null=True)
    job_type = models.ForeignKey("JobType", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name="Company", on_delete=models.CASCADE)
    is_company_name_hidden = models.BooleanField(default=False)
    created_date = models.DateField(auto_now=True)
    job_description = models.TextField(max_length=500, null=True)
    is_active = models.BooleanField(default=True)


class JobType(models.Model):
    job_type = models.CharField(max_length=50)
    job_type_english = models.CharField(max_length=50, null=True)

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
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, null=True)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)

    def __str__(self):
        return f"job - {self.job_post.job_title}, city - {self.city}, country - {self.country}"


class JobConversation(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, null=True)
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversation_employer")
    seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversation_seeker")
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"job - {self.job.job_title}; ({self.employer.email}, {self.seeker.email})"


class ConversationMessage(models.Model):
    conversation = models.ForeignKey(JobConversation, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_from_me"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_to_me"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"From {self.from_user.email} to {self.to_user.email}: {self.message} [{self.timestamp}]"
