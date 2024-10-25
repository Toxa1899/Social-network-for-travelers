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

from django.utils import timezone


class PostCRUDTest(APITestCase):
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
        self.country = Country.objects.create(name="Kyrgyzstan")
        self.client.force_authenticate(user=self.user)

        self.url_list = reverse("posts-list")
        self.url_detail = lambda pk: reverse("posts-detail", kwargs={"pk": pk})

    def test_create_post(self):
        """Тест на создание поста"""
        data = {
            "author": self.user.id,
            "country": self.country.id,
            "topic": "Test Topic",
            "body": "Test Body",
        }
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)

    def test_retrieve_post(self):
        """Тест на получение поста"""
        post = Post.objects.create(
            author=self.user,
            country=self.country,
            topic="Test",
            body="Test Body",
        )
        response = self.client.get(self.url_detail(post.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["topic"], "Test")

    def test_update_post(self):
        """Тест на обновление поста"""
        post = Post.objects.create(
            author=self.user,
            country=self.country,
            topic="Old Topic",
            body="Old Body",
        )
        data = {"topic": "Updated Topic"}
        response = self.client.patch(
            self.url_detail(post.id), data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.topic, "Updated Topic")

    def test_delete_post(self):
        """Тест на удаление поста"""
        post = Post.objects.create(
            author=self.user,
            country=self.country,
            topic="Test",
            body="Test Body",
        )
        response = self.client.delete(self.url_detail(post.id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), 0)

    def test_change_rating(self):
        """
        тест на добавление рейтинга
        """
        post = Post.objects.create(
            author=self.user,
            country=self.country,
            topic="Test",
            body="Test Body",
        )

        data = {"rating_change": "increase"}
        response = self.client.post(f"/api/v1/posts/{post.id}/rating/", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Rating.objects.all().exists())


class DisablePostTest(APITestCase):
    """
    Тест отключения видимости поста
    """

    def setUp(self):
        self.client = APIClient()
        self.email = "admin@gmail.com"
        self.password = "testpassword"
        self.user = CustomUser.objects.create_superuser(
            email=self.email, password=self.password
        )

        self.client.force_authenticate(user=self.user)
        self.url = lambda pk: reverse("disable", kwargs={"pk": pk})
        self.country = Country.objects.create(name="Kyrgyzstan")
        self.post = Post.objects.create(
            author=self.user,
            country=self.country,
            topic="Test",
            body="Test Body",
        )

    def test_disable_post(self):
        """
        отключение поста
        """
        response = self.client.post(self.url(self.post.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.filter(is_visible=False).exists(), True)


class PostLiftTest(APITestCase):
    """
    Тест поднятия поста
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.email = "admin@gmail.com"
        self.password = "testpassword"
        self.user = CustomUser.objects.create_superuser(
            email=self.email, password=self.password
        )

        self.client.force_authenticate(user=self.user)

        self.country = Country.objects.create(name="Kyrgyzstan")
        self.post = Post.objects.create(
            author=self.user,
            country=self.country,
            topic="Test",
            body="Test Body",
        )
        self.now = timezone.now()

    def test_lift(self):
        """
        Тест создания lift post
        """
        url = reverse("lift-list")
        day_of_week = DaysOfWeek.objects.create(days_of_week="Monday")

        data = {
            "post": self.post.id,
            "start_date": self.now.date(),
            "end_date": self.now.date(),
            "time": self.now.time(),
            "days_of_week": [day_of_week.id],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PostLiftSettings.objects.count(), 1)
