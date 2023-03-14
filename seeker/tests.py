import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from seeker.api.services.handle_seeker_profile import get_seeker_profile_by_user_account
from users.models import UserType
from users.api.services import handle_user
from seeker.models import EducationDetail, ExperienceDetails, SkillSet, SeekerSkillSet


class BaseTest(APITestCase):
    def setUp(self) -> None:
        user_type = UserType.objects.create(user_type_name="seeker", has_additional_profile=True)
        self.client = APIClient()

        self.credentials = {
            "email": "user@gmail.com", "password": "user", "user_type_id": user_type.id
        }
        response = self.client.post(reverse("auth_user_create"), data=json.dumps(self.credentials),
                                    content_type="application/json")

        self.user = handle_user.get_user_by_email(response.data['email'])

        # self.access_token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')


class SeekerProfileTests(BaseTest):

    def test_get_seeker_profile(self):
        response = self.client.get(reverse("get_seeker_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user_account"], self.user.id)

    def test_edit_seeker_profile(self):
        data = {
            "first_name": "user",
            "last_name": "user",
            "current_salary": 1000,
        }

        response = self.client.patch(reverse("edit_seeker_profile"), data=data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user_account"], self.user.id)
        self.assertEqual(response.data["first_name"], "user")
        self.assertEqual(response.data["last_name"], "user")
        self.assertEqual(response.data["current_salary"], 1000)


class SeekerEducationTests(BaseTest):

    def setUp(self):
        super().setUp()
        self.education = EducationDetail.objects.create(profile_account=get_seeker_profile_by_user_account(self.user),
                                                        certificate_degree_name='certificate_degree_name',
                                                        major="bachelor", institute_university_name="KPI")

    def test_get_seeker_educations(self):
        response = self.client.get(reverse("get_seeker_all_educations"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_add_seeker_education(self):
        data = {
            "certificate_degree_name": "certificate_degree_name1",
            "major": "bachelor",
            "institute_university_name": "KPI"
        }

        response = self.client.post(reverse("create_seeker_education"), data=data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["certificate_degree_name"], "certificate_degree_name1")
        self.assertEqual(response.data["major"], "bachelor")
        self.assertEqual(response.data["institute_university_name"], "KPI")

    def test_edit_seeker_education(self):
        data = {
            "certificate_degree_name": "certificate_degree_name_edited",
            "major": "bachelor_edited",
            "institute_university_name": "KPI_edited"
        }

        response = self.client.patch(reverse("edit_seeker_education", kwargs={"pk": self.education.id}), data=data,
                                     format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["certificate_degree_name"], "certificate_degree_name_edited")
        self.assertEqual(response.data["major"], "bachelor_edited")
        self.assertEqual(response.data["institute_university_name"], "KPI_edited")

    def test_delete_seeker_education(self):
        response = self.client.delete(reverse("delete_seeker_education", kwargs={"pk": self.education.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Successful")


class SeekerExperienceTests(BaseTest):

    def setUp(self):
        super().setUp()
        self.experience = ExperienceDetails.objects.create(
            profile_account=get_seeker_profile_by_user_account(self.user),
            start_date='2022-04-17',
            end_date="2022-04-17", job_title="Django BackEnd Developer")

    def test_get_seeker_experience(self):
        response = self.client.get(reverse("get_all_seeker_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_add_seeker_experience(self):
        data = {
            "start_date": "2022-05-22",
            "end_date": "2022-04-17",
            "job_title": "JavaScript Web Developer"
        }

        response = self.client.post(reverse("create_seeker_experience"), data=data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["start_date"], "2022-05-22")
        self.assertEqual(response.data["end_date"], "2022-04-17")
        self.assertEqual(response.data["job_title"], "JavaScript Web Developer")

    def test_edit_seeker_experience(self):
        data = {
            "start_date": "2022-05-20",
            "end_date": "2022-04-01",
            "job_title": "JavaScript Web Developer"
        }

        response = self.client.patch(reverse("edit_seeker_experience", kwargs={"pk": self.experience.id}), data=data,
                                     format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["start_date"], "2022-05-20")
        self.assertEqual(response.data["end_date"], "2022-04-01")
        self.assertEqual(response.data["job_title"], "JavaScript Web Developer")

    def test_delete_seeker_education(self):
        response = self.client.delete(reverse("delete_seeker_experience", kwargs={"pk": self.experience.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Successful")


class SkillsetTests(BaseTest):

    def setUp(self):
        super().setUp()
        self.skillset1 = SkillSet.objects.create(name="Python")
        self.skillset2 = SkillSet.objects.create(name="Django")
        self.skillset3 = SkillSet.objects.create(name="Flask")

    def test_get_seeker_experience(self):
        response = self.client.get(reverse("get_all_skillsets"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class SeekerSkillsetTests(BaseTest):

    def setUp(self):
        super().setUp()
        self.skillset1 = SkillSet.objects.create(name="Python")
        self.skillset2 = SkillSet.objects.create(name="Django")
        self.skillset3 = SkillSet.objects.create(name="Flask")
        self.skillset4 = SkillSet.objects.create(name="FastAPI")

        self.seeker_skillset1 = SeekerSkillSet.objects.create(
            profile_account=get_seeker_profile_by_user_account(self.user), skill_set=self.skillset1, skill_level=4)
        self.seeker_skillset2 = SeekerSkillSet.objects.create(
            profile_account=get_seeker_profile_by_user_account(self.user), skill_set=self.skillset2, skill_level=5)
        self.seeker_skillset3 = SeekerSkillSet.objects.create(
            profile_account=get_seeker_profile_by_user_account(self.user), skill_set=self.skillset3, skill_level=5)

    def test_get_seeker_experience(self):
        response = self.client.get(reverse("get_seeker_skillset"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_add_seeker_experience(self):
        data = [
            {"id": self.skillset4.id,
             "skill_level": 5},

        ]

        response = self.client.post(reverse("create_seeker_skillset"), data=data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "Successful")

    #
    def test_edit_seeker_experience(self):
        data = [
            {"id": self.skillset4.id,
             "skill_level": 4},

        ]

        response = self.client.put(reverse("edit_seeker_skillset"), data=data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Successful")

    def test_delete_seeker_education(self):
        response = self.client.delete(reverse("delete_seeker_skillset"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Successful")
