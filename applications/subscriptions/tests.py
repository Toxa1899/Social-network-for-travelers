from rest_framework.test import (
    APITestCase,
    APIClient,
)
from applications.account.models import CustomUser
from django.urls import reverse
from applications.countries.models import Country
from applications.product.models import (
    Post,
    Rating,
    DaysOfWeek,
    PostLiftSettings,
)


class SubscriptionTest(APITestCase):
    """
    Тест crad поста
    """

    def setUp(self):
        self.client = APIClient()
        self.email = "admin@gmail.com"
        self.password = "testpassword"
        self.user = CustomUser.objects.create_user(
            email=self.email, password=self.password
        )

        self.client.force_authenticate(user=self.user)
        self.url_list = reverse("posts-list")
        self.url_detail = lambda pk: reverse("posts-detail", kwargs={"pk": pk})
