from rest_framework.test import (
    APITestCase,
    APIClient,
)
from applications.account.models import CustomUser
from django.urls import reverse
from applications.countries.models import Country
from applications.product.models import Tag

from applications.subscriptions.models import Subscription


class SubscriptionTest(APITestCase):
    """
    Тест crad поста
    """

    def setUp(self):
        self.client = APIClient()
        self.email = "admin@gmail.com"
        self.email2 = "admin2@gmail.com"
        self.password = "testpassword"
        self.user = CustomUser.objects.create_user(
            email=self.email, password=self.password
        )

        self.user2 = CustomUser.objects.create_user(
            email=self.email2, password=self.password
        )

        self.country = Country.objects.create(name="Kyrgyzstan")

        self.tag = Tag.objects.create(name="кринж")

        self.client.force_authenticate(user=self.user)
        self.url = reverse("subscriptions-list")

    def test_sub_country_and_unsub(self):
        data = {"country": self.country.id}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Subscription.objects.exists())

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Subscription.objects.exists())

    def test_sub_tag_and_unsub(self):
        data = {"tag": self.tag.id}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Subscription.objects.exists())

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Subscription.objects.exists())

    def test_sub_user_and_unsub(self):
        data = {"subscribed_user": self.user2.id}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Subscription.objects.exists())

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Subscription.objects.exists())

    def test_many_params(self):
        data = {
            "subscribed_user": self.user2.id,
            "tag": self.tag.id,
            "country": self.country.id,
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Subscription.objects.exists())

    def test_two_sub(self):
        data = {
            "subscribed_user": self.user2.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)

        data = {
            "tag": self.tag.id,
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Subscription.objects.count(), 2)
