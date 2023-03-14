import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from users.models import UserType


class AuthTests(APITestCase):

    def setUp(self) -> None:
        user_type = UserType.objects.create(user_type_name="seeker", has_additional_profile=True)
        self.client = APIClient()

        self.credentials = {
            "email": "user@gmail.com", "password": "user", "user_type_id": user_type.id
        }
        response = self.client.post(reverse("auth_user_create"), data=json.dumps(self.credentials),
                                    content_type="application/json")

        # self.access_token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')

    def test_get_user_info(self):
        response = self.client.get(reverse("user_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.data.keys())
        self.assertEqual(response.data.get("email"), self.credentials["email"])
        self.assertEqual(response.data.get("user_type"), self.credentials["user_type_id"])

    #
    def test_change_user_info(self):
        data = {
            "date_of_birth": "2003-03-31",
            "gender": "male",
        }

        response = self.client.patch(reverse("user_profile"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("date_of_birth"), "2003-03-31")
        self.assertEqual(response.data.get("gender"), "male")

    def test_get_user_log(self):
        response = self.client.get(reverse("user_log"))

        data = response.data
        self.assertEqual(data.get("user_account"), 3)
        self.assertEqual(response.status_code, 200)

    def test_get_user_types(self):
        response = self.client.get(reverse("get_all_user_types"))

        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
