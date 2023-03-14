import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from users.models import UserType
from users.api.services import handle_user
from company.models import Company, BusinessStream


class CompanyTests(APITestCase):

    def setUp(self) -> None:
        user_type = UserType.objects.create(user_type_name="employer", has_additional_profile=False)
        self.client = APIClient()

        self.credentials = {
            "email": "user@gmail.com", "password": "user", "user_type_id": user_type.id
        }
        response = self.client.post(reverse("auth_user_create"), data=json.dumps(self.credentials),
                                    content_type="application/json")

        self.user = handle_user.get_user_by_email(response.data['email'])

        self.business_stream = BusinessStream.objects.create(business_stream_name="Аутсорс",
                                                             business_stream_english_name="Outsource")

        self.company1 = Company.objects.create(company_name="company_name", user_account=self.user,
                                               business_stream=self.business_stream)
        #
        # self.access_token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')

    def test_get_companies_for_user(self):
        response = self.client.get(reverse("get_all_companies"))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data), 1)

    def test_create_company(self):
        data = {
            "company_name": "some company name",
            "business_stream": self.business_stream.id,
            "profile_description": "some profile description"
        }
        response = self.client.post(reverse("create_company"), data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["company_name"], "some company name")
        self.assertEqual(response.data["profile_description"], "some profile description")

    def test_change_company(self):
        data = {
            "company_name": "some company name edited",
            "profile_description": "some profile description edited"
        }
        response = self.client.patch(reverse("edit_company", kwargs={"pk": self.company1.id}), data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["company_name"], "some company name edited")
        self.assertEqual(response.data["profile_description"], "some profile description edited")

    def test_delete_company(self):
        response = self.client.delete(reverse("delete_company", kwargs={"pk": self.company1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "successful")

    def test_get_all_business_streams(self):
        response = self.client.get(reverse("get_all_business_streams"))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data), 1)