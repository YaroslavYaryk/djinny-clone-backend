from django.shortcuts import get_object_or_404

from job.models import JobPost


def get_job_post_by_id(pk):
    return get_object_or_404(JobPost, pk=pk)


def get_job_post_by_id_for_user(pk, user):
    return get_object_or_404(JobPost, pk=pk, posted_by=user)


def get_job_posts_for_user(user):
    return JobPost.objects.filter(posted_by=user)


def delete_job_post(pk, user):
    get_job_post_by_id_for_user(pk, user).delete()


def get_jobs_by_list_ids(list_ids: list):
    return JobPost.objects.filter(id__in=list_ids)


def get_all_jobs():
    return JobPost.objects.all()
