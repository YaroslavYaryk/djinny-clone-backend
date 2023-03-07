from itertools import compress

from job.models import JobPost, JobLocation, JobType, JobPostSkillSet
from .handle_seeker_profile import get_seeker_profile_by_user_account
from .handle_seeker_experience import get_seeker_experience_years
from .handle_skillset import get_seeker_skillset
from job.api.services import handle_job_post, handle_job_skillset


def get_recommended_jobs_for_seeker(user):
    seeker_experience = get_seeker_experience_years(user)
    seeker_skillset = get_seeker_skillset(user)
    jobs = handle_job_post.get_all_jobs()

    seeker_skillset_pure_object = [el.skill_set for el in seeker_skillset]

    suitable_seeker_experience = seeker_experience + 0.5

    jobs_recommendation = jobs.filter(job_post_skill__skill_set__in=seeker_skillset_pure_object,
                                      experience_years_required__lte=suitable_seeker_experience).distinct()

    return jobs_recommendation


def get_searched_jobs(data, user):
    queryset = JobPost.objects.all().select_related("company").prefetch_related("job_post_skill")
    if data.get("title"):
        queryset = handle_job_post.filter_job_queryset_by_title_job(queryset, data["title"])
    if data.get("technologies"):
        queryset = handle_job_post.filter_job_queryset_by_skillset_ids(queryset, data["technologies"])
    if data.get("experience"):
        queryset = handle_job_post.filter_job_queryset_by_experience(queryset, data["experience"])
    if data.get("salary"):
        queryset = handle_job_post.filter_job_queryset_by_salary(queryset, data["salary"])
    if data.get("company_type"):
        queryset = handle_job_post.filter_job_queryset_by_company_type(queryset, data["company_type"])

    return queryset
