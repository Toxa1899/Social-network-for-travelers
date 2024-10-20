from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
import logging

# Create your tests here.

logger = logging.getLogger(__name__)


class UserRegisterTest(APITestCase):
    def setUp(self):
        self.url = reverse("register")
        self.User = get_user_model()

    def test_register_success(self):
        data = {
            "email": "testuser@gmail.com",
            "password": "a(FV)4ha[i97_Ck.CR.I<4r",
            "password2": "a(FV)4ha[i97_Ck.CR.I<4r",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, "Вы успешно зарегистрировались")

        self.assertEqual(self.User.objects.count(), 1)
        self.assertEqual(self.User.objects.get().email, "testuser@gmail.com")

    def test_register_different_password(self):
        data = {
            "email": "testuser@gmail.com",
            "password": "a(FV)4ha[i97_Ck.CR.I<4r",
            "password2": "a(FV)4ha[i97_Ck.CR.I<4r223",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"][0], "Пароли не совпадают"
        )
        self.assertEqual(self.User.objects.count(), 0)

    def test_valid_email(self):
        data = {
            "email": "1",
            "password": "a(FV)4ha[i97_Ck.CR.I<4r",
            "password2": "a(FV)4ha[i97_Ck.CR.I<4r223",
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["email"][0], "Enter a valid email address."
        )
