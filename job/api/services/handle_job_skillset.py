from job.models import JobPostSkillSet
from .static_dunctional import JobSkillSet


def get_job_skillset(job_id):
    return JobPostSkillSet.objects.filter(job_post__id=job_id).select_related("skill_set")


def get_class_list_from_js(data, job_id):
    try:
        return [
            JobPostSkillSet(skill_set_id=elem["id"], job_post_id=job_id, skill_level=elem['level']) for elem in data
        ]
    except Exception:
        return []


def create_job_skillset(skillset: JobSkillSet, job_id):
    JobPostSkillSet.objects.create(skill_set_id=skillset.skillset_id, skill_level=skillset.level, job_post_id=job_id)


def add_skillsets_to_job(data):
    JobPostSkillSet.objects.bulk_create(data)


def delete_job_skillset(pk):
    get_job_skillset(pk).delete()


def get_job_skillset_by_name(name):
    try:
        return JobPostSkillSet.objects.get(skill_set__name=name)
    except Exception:
        return None
