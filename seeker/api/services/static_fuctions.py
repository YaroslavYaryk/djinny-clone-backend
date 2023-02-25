def get_errors_as_string(serializer):
    return "\n".join(
        [el.title() for values in serializer.errors.values() for el in values]
    )


class SeekerSkillset:
    def __init__(self, skill_set_id, skill_level):
        self.skill_set_id = skill_set_id
        self.skill_level = skill_level


def turn_js_list_objects_to_python(objects_list):
    try:
        return [
            SeekerSkillset(el["id"], el["skill_level"]) for el in objects_list
        ]
    except Exception:
        return []
