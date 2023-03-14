import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from seeker.models import SkillSet
from users.models import UserType
from users.api.services import handle_user
from job.models import JobType, JobPost, JobLocation, JobPostSkillSet, ConversationMessage, JobConversation
from company.models import Company


class BaseTest(APITestCase):
    def setUp(self) -> None:
        self.user_type = UserType.objects.create(user_type_name="employer", has_additional_profile=False)
        self.user_type2 = UserType.objects.create(user_type_name="seeker", has_additional_profile=True)
        self.client = APIClient()

        self.credentials = {
            "email": "user@gmail.com", "password": "user", "user_type_id": self.user_type.id
        }
        response = self.client.post(reverse("auth_user_create"), data=json.dumps(self.credentials),
                                    content_type="application/json")

        self.user = handle_user.get_user_by_email(response.data['email'])

        # self.access_token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')


class BaseJobTest(BaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.job_type = JobType.objects.create(job_type="Outsource",
                                               job_type_english="Аутсорсингова")

        self.company = Company.objects.create(user_account=self.user, company_name="company_name")

        self.job = JobPost.objects.create(posted_by=self.user,
                                          job_title='Django developer',
                                          job_type=self.job_type, company=self.company)


class JobTypeTests(BaseTest):

    def setUp(self):
        super().setUp()
        self.job_type = JobType.objects.create(job_type="Outsource",
                                               job_type_english="Аутсорсингова")

    def test_get_job_types(self):
        response = self.client.get(reverse("get_all_job_types"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class JobTests(BaseJobTest):

    def setUp(self):
        super().setUp()

    def test_get_jobs(self):
        response = self.client.get(reverse("get_all_job_posts"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_add_job(self):
        data = {
            "job_title": "job_title",
            "job_type": self.job_type.id,
            "company": self.company.id,
            "job_description": "job_description"
        }

        response = self.client.post(reverse("create_one_job_post"), data=data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["job_title"], "job_title")
        self.assertEqual(response.data["job_type"], self.job_type.id)
        self.assertEqual(response.data["company"], self.company.id)
        self.assertEqual(response.data["job_description"], "job_description")

    def test_edit_job(self):
        data = {
            "job_title": "job_title_edited",
            "job_type": self.job_type.id,
            "company": self.company.id,
            "job_description": "job_description_edited"
        }

        response = self.client.patch(reverse("edit_one_job_post", kwargs={"pk": self.job.id}), data=data,
                                     format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["job_title"], "job_title_edited")
        self.assertEqual(response.data["job_type"], self.job_type.id)
        self.assertEqual(response.data["company"], self.company.id)
        self.assertEqual(response.data["job_description"], "job_description_edited")

    def test_delete_seeker_education(self):
        response = self.client.delete(reverse("delete_one_job_post", kwargs={"pk": self.job.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "successful")


class JobActivityTests(BaseJobTest):

    def setUp(self):
        super().setUp()

    def test_get_job_activity(self):
        response = self.client.get(reverse("get_job_activity", kwargs={"pk": self.job.id}))
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["job_post"], self.job.id)


class JobLocationTests(BaseJobTest):

    def setUp(self):
        super().setUp()
        self.job_location = JobLocation.objects.create(
            job_post=self.job,
            country="Ukraine",
            city="Kyiv",
            street_address="street_address"
        )

    def test_get_job_locations(self):
        response = self.client.get(reverse("get_all_job_location", kwargs={"id": self.job.id}), )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_add_job_location(self):
        data = {
            "country": "Ukraine",
            "city": "Rivne",
            "street_address": "street_address"
        }

        response = self.client.post(reverse("create_job_location", kwargs={"pk": self.job.id}), data=data,
                                    format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["country"], "Ukraine")
        self.assertEqual(response.data["city"], "Rivne")
        self.assertEqual(response.data["street_address"], "street_address")

    def test_edit_seeker_experience(self):
        data = {
            "country": "Ukraine",
            "city": "Lutsk",
            "street_address": "street_address"
        }

        response = self.client.patch(
            reverse("edit_job_location", kwargs={"pk": self.job.id, "location_id": self.job_location.id}), data=data,
            format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["country"], "Ukraine")
        self.assertEqual(response.data["city"], "Lutsk")
        self.assertEqual(response.data["street_address"], "street_address")

    def test_delete_seeker_education(self):
        response = self.client.delete(
            reverse("delete_job_location", kwargs={"pk": self.job.id, "location_id": self.job_location.id}), )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "successful")


class JobSkillsetTests(BaseJobTest):

    def setUp(self):
        super().setUp()
        self.skillset1 = SkillSet.objects.create(name="Python")
        self.skillset2 = SkillSet.objects.create(name="Django")
        self.skillset3 = SkillSet.objects.create(name="Flask")

        self.job_skillset1 = JobPostSkillSet.objects.create(skill_set=self.skillset1, job_post=self.job, skill_level=5)
        self.job_skillset2 = JobPostSkillSet.objects.create(skill_set=self.skillset2, job_post=self.job, skill_level=4)

    def test_get_job_skillset(self):
        response = self.client.get(reverse("get_all_job_skillset", kwargs={"pk": self.job.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_add_job_skillset(self):
        data = [
            {
                "id": self.skillset3.id,
                "level": 4
            }
        ]

        response = self.client.post(reverse("create_job_skillset", kwargs={"pk": self.job.id}), data=data,
                                    format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "successful")

    def test_edit_job_skillset(self):
        data = [
            {
                "id": self.skillset3.id,
                "level": 5
            }
        ]

        response = self.client.put(reverse("edit_job_skillset", kwargs={"pk": self.job.id}), data=data,
                                   format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "successful")

    def test_delete_job_skillset(self):
        response = self.client.delete(reverse("delete_job_skillset", kwargs={"pk": self.job.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "successful")


class JobConversationTests(BaseJobTest):

    def setUp(self):
        super().setUp()
        self.seeker = get_user_model().objects.create(email="seeker@gmail.com", password="seeker",
                                                      user_type=self.user_type2)
        self.conversation = JobConversation.objects.create(job=self.job, employer=self.user, seeker=self.seeker)

    def test_get_all_conversations(self):
        response = self.client.get(reverse("get_all_conversations"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_add_seeker_experience(self):
        response = self.client.post(reverse("create_one_conversations", kwargs={
            "job_id": self.job.id, "user_type": "employer", "user_id": self.seeker.id
        }), format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["job"], self.job.id)
        self.assertEqual(response.data["employer"], self.user.id)
        self.assertEqual(response.data["seeker"], self.seeker.id)

    def test_delete_job_conversation(self):
        response = self.client.delete(
            reverse("delete_one_conversations", kwargs={"conversation_id": self.conversation.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "successful")


class ConversationMessageTests(BaseJobTest):

    def setUp(self):
        super().setUp()
        self.seeker = get_user_model().objects.create(email="seeker@gmail.com", password="seeker",
                                                      user_type=self.user_type2)
        self.conversation = JobConversation.objects.create(job=self.job, employer=self.user, seeker=self.seeker)
        self.message = ConversationMessage.objects.create(conversation=self.conversation, message="message",
                                                          from_user=self.user, to_user=self.seeker)

    def test_get_all_messages(self):
        response = self.client.get(reverse("get_all_messages_for_conversation", kwargs={"pk": self.conversation.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_add_message(self):
        data = {
            "message": "message",
            "from_user": self.user.id, "to_user": self.seeker.id
        }

        response = self.client.post(reverse("add_message_to_conversation", kwargs={
            "pk": self.conversation.id
        }), data=data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "message")
        self.assertEqual(response.data["from_user"], self.user.id)
        self.assertEqual(response.data["to_user"], self.seeker.id)

    def test_edit_message(self):
        data = {
            "message": "message edited",
            "from_user": self.user.id, "to_user": self.seeker.id
        }

        response = self.client.put(reverse("edit_message_to_conversation", kwargs={
            "pk": self.conversation.id, "message_id": self.message.id
        }), data=data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "message edited")
        self.assertEqual(response.data["from_user"], self.user.id)
        self.assertEqual(response.data["to_user"], self.seeker.id)

    def test_delete_message(self):
        response = self.client.delete(
            reverse("delete_message_to_conversation", kwargs={
                "pk": self.conversation.id, "message_id": self.message.id
            }))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "successful")
