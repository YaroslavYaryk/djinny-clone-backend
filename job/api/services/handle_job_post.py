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


def filter_job_queryset_by_title_job(queryset, title):
    return queryset.filter(job_title__icontains=title)


def filter_job_queryset_by_skillset_ids(queryset, data):
    return queryset.filter(job_post_skill__skill_set__id__in=data).distinct()


def filter_job_queryset_by_experience(queryset, data):
    return queryset.filter(experience_years_required__gte=data["bottom"], experience_years_required__lte=data["top"])


def filter_job_queryset_by_salary(queryset, data):
    return queryset.filter(salary__gte=data["bottom"], salary__lte=data["top"])


def filter_job_queryset_by_company_type(queryset, data):
    return queryset.filter(company__business_stream_id__in=data)
