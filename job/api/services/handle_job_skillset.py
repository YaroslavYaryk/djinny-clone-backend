from job.models import JobPostSkillSet
from .static_dunctional import JobSkillSet


def get_job_skillset(job_id):
    return JobPostSkillSet.objects.filter(job_post__id=job_id)


def get_class_list_from_js(data):
    try:
        return [
            JobSkillSet(elem["id"], elem['level']) for elem in data
        ]
    except Exception:
        return []


def create_job_skillset(skillset: JobSkillSet, job_id):
    JobPostSkillSet.objects.create(skill_set_id=skillset.skillset_id, skill_level=skillset.level, job_post_id=job_id)


def add_skillsets_to_job(data, pk):
    for skillset in data:
        create_job_skillset(skillset, pk)


def delete_job_skillset(pk):
    get_job_skillset(pk).delete()
