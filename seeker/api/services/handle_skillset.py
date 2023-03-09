from django.shortcuts import get_object_or_404

from .handle_seeker_profile import get_seeker_profile_by_user_account
from seeker.models import SeekerSkillSet, SkillSet
from .static_fuctions import SeekerSkillset as SeekerSkillsetObject


def get_skillset_by_id(pk):
    return get_object_or_404(SkillSet, pk=pk)


def get_all_skill_sets():
    return SkillSet.objects.all()


def get_seeker_skillset(user):
    profile_account = get_seeker_profile_by_user_account(user)
    return SeekerSkillSet.objects.filter(profile_account=profile_account)


def turn_js_list_objects_to_python(objects_list, user):
    profile_account = get_seeker_profile_by_user_account(user)
    try:
        return [
            SeekerSkillSet(skill_set_id=elem["id"], profile_account=profile_account, skill_level=elem["level"]) for
            elem in
            objects_list
        ]
    except Exception as ex:
        return []


def create_seeker_skillset(profile_account, skillset: SeekerSkillsetObject):
    SeekerSkillSet.objects.create(profile_account=profile_account, skill_set_id=skillset.skill_set_id,
                                  skill_level=skillset.skill_level)


def add_skillsets_to_seeker_skillset(skillsets):
    SeekerSkillSet.objects.bulk_create(skillsets)


def delete_seeker_skillset(user):
    get_seeker_skillset(user).delete()
