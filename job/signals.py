from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from job.models import JobPost, JobPostActivity
from job.api.services import handle_job_type_and_activity


@receiver(post_save, sender=JobPost)
def create_job_activity(sender, instance: JobPost, created, **kwargs):
    if created:
        handle_job_type_and_activity.create_job_post_activity(instance)
