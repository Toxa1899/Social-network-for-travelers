from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from applications.account.models import CustomUser
from applications.comment.models import Comment
from applications.product.models import Post
from applications.countries.models import Country


class CommentCRUDTest(APITestCase):
    """
    Тест CRUD коментов
    """

    def setUp(self):
        self.email = "test@gmail.com"
        self.password = "passwordpassword"
        self.user = CustomUser.objects.create_user(
            email=self.email, password=self.password
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.url = reverse("comment-list")
        self.country = Country.objects.create(name="Kyrgyzstan")
        self.post = Post.objects.create(
            author=self.user,
            country=self.country,
            topic="Old Topic",
            body="Old Body",
        )

    def test_create_comment(self):
        """
        тест создание комента
        """
        data = {
            "author": self.user.id,
            "post": self.post.id,
            "content": "test-comment",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)

    def test_retrive_comment_no_author(self):
        """
        тест получение не своих коментов
        """
        user_no_author = CustomUser.objects.create(
            email="noauthor@gmail.com", password="passwordpassword"
        )

        Comment.objects.create(
            author=user_no_author, post=self.post, content="test"
        )

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.json()["count"], 0)

    def test_retrive_comment_author(self):
        """
        тест получение  своих коментов
        """
        Comment.objects.create(
            author=self.user, post=self.post, content="test"
        )

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.json()["count"], 1)
