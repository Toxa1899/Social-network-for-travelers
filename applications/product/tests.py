from rest_framework.test import (
    APITestCase,
    APIRequestFactory,
    force_authenticate,
    APIClient,
)
from applications.account.models import CustomUser
from django.urls import reverse
from applications.countries.models import Country
from applications.product.models import Post
from applications.product.views import PostModelViewSet


class PostCRUDTest(APITestCase):
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
        post = Post.objects.create(
            author=self.user,
            country=self.country,
            topic="Test",
            body="Test Body",
        )

        data = {"rating_change": "increase"}
        response = self.client.post(f"/api/v1/posts/{post.id}/rating/", data)
        self.assertEqual(response.status_code, 200)
