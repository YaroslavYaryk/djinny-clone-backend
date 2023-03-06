from django.shortcuts import get_object_or_404

from job.models import JobType, JobPostActivity


def get_job_type_by_id(pk):
    return get_object_or_404(JobType, pk=pk)


def get_all_job_types():
    return JobType.objects.all()


def create_job_post_activity(job_post):
    JobPostActivity.objects.create(job_post=job_post)


def get_activity_for_job(pk, user):
    return get_object_or_404(JobPostActivity, job_post__pk=pk, job_post__posted_by=user)
