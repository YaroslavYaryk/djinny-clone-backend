from itertools import compress

from job.models import JobPost, JobLocation, JobType, JobPostSkillSet
from .handle_seeker_profile import get_seeker_profile_by_user_account
from .handle_seeker_experience import get_seeker_experience_years
from .handle_skillset import get_seeker_skillset
from job.api.services import handle_job_post, handle_job_skillset


def compare_skillsets(seeker_data, job_skillset, job):
    seeker_skillset, seeker_experience = seeker_data.values()

    job_skillset_names = [skill.skill_set.name for skill in job_skillset]
    job_skillset_length = job_skillset.count()

    if not job_skillset_length:
        return False

    suitable_jobs = 0
    for skill in seeker_skillset:
        if skill.skill_set.name in job_skillset_names and seeker_experience + 0.5 >= job.experience_years_required:
            suitable_jobs += 1

    return True if suitable_jobs / job_skillset_length > 0.6 else False


def get_recommended_jobs_for_seeker(user):
    seeker_experience = get_seeker_experience_years(user)
    seeker_skillset = get_seeker_skillset(user)
    jobs = handle_job_post.get_all_jobs()

    seeker_data = {
        "seeker_skillset": seeker_skillset,
        "seeker_experience": seeker_experience
    }

    jobs_recommendation = [compare_skillsets(seeker_data, handle_job_skillset.get_job_skillset(job.id), job) for job
                           in
                           jobs]

    job_ids = [el.id for el in compress(jobs, jobs_recommendation)]
    return handle_job_post.get_jobs_by_list_ids(job_ids)
