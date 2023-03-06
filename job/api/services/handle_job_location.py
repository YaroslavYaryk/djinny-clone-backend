from django.shortcuts import get_object_or_404

from job.models import JobLocation


def get_location_for_job(pk, location_id, user):
    return get_object_or_404(JobLocation, pk=location_id, job_post__pk=pk, job_post__posted_by=user)


def get_all_job_locations(pk, user):
    return JobLocation.objects.filter(job_post__pk=pk, job_post__posted_by=user)


def delete_job_location(pk, location_id, user):
    get_location_for_job(pk, location_id, user).delete()
