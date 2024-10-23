from rest_framework.test import (
    APITestCase,
    APIRequestFactory,
    force_authenticate,
)
from applications.countries.views import (
    CountriesAllModelViewSet,
    CountriesModelViewSet,
)
from rest_framework.authentication import get_user_model
from django.urls import reverse
from applications.countries.models import Country
from applications.product.models import Post
from rest_framework import status

User = get_user_model()


class CountryAllTest(APITestCase):
    """
    Тест CRAD Стран
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.email = "admin@gmail.com"
        self.password = "testpassword"
        self.url = reverse("countries_all-list")
        self.user = User.objects.create_user(
            email=self.email, password=self.password
        )

    def testy_create_country_no_admin(self):
        """
        Тест на создание  страны - не админ пользователем
        """
        data = {"name": "kyrgyzstan"}

        request = self.factory.post(self.url, data, format="json")
        view = CountriesAllModelViewSet.as_view({"post": "create"})
        force_authenticate(request, self.user)
        response = view(request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )
        self.assertEqual(Country.objects.count(), 0)

    def testy_create_country(self):
        """
        Тест на создание страны -  админ пользователем
        """
        data = {"name": "kyrgyzstan"}
        self.email = "test@gmail.com"
        self.user = User.objects.create_superuser(
            email=self.email, password=self.password
        )
        request = self.factory.post(self.url, data, format="json")
        view = CountriesAllModelViewSet.as_view({"post": "create"})
        force_authenticate(request, self.user)
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Country.objects.count(), 1)

    def test_del_country(self):
        """
        Тест на удаление страны
        """

        country = Country.objects.create(name="kyrgyzstan")
        url = reverse("countries_all-detail", args=[country.id])
        request = self.factory.delete(url, format="json")

        self.user = User.objects.create_superuser(
            email="admin2@gmail.com", password=self.password
        )
        force_authenticate(request, self.user)

        view = CountriesAllModelViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=country.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Country.objects.count(), 0)

    def test_del_country(self):
        """
        Тест на обновление страны
        """
        country = Country.objects.create(name="kyrgyzstan")

        url = reverse("countries_all-detail", args=[country.id])
        data = {"name": "kyrgyzstan-patch"}
        self.assertEqual(country.name, "kyrgyzstan")

        request = self.factory.patch(url, data, format="json")
        self.user = User.objects.create_superuser(
            email="admin2@gmail.com", password=self.password
        )
        force_authenticate(request, self.user)

        view = CountriesAllModelViewSet.as_view({"patch": "partial_update"})
        response = view(request, pk=country.id)

        country.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(country.name, "kyrgyzstan-patch")


class Countries(APITestCase):
    """
    Тест на список тех стран, для которых был
    создан один и более пост
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.email = "admin@gmail.com"
        self.password = "testpassword"
        self.url = reverse("countries_all-list")
        self.user = User.objects.create_user(
            email=self.email, password=self.password
        )

    def test_get_countries(self):
        """
        проверка на получение стран
        """
        request = self.factory.get(self.url, format="json")
        force_authenticate(request, self.user)
        views = CountriesModelViewSet.as_view({"get": "list"})
        response = views(request)
        self.assertEqual(response.data["results"], [])

    def test_get_countries_data(self):
        """
        проверка на получение стран
        """
        country = Country.objects.create(name="kyrgyzstan")
        Post.objects.create(
            author=self.user, country=country, topic="test", body="test"
        )
        request = self.factory.get(self.url, format="json")
        force_authenticate(request, self.user)
        views = CountriesModelViewSet.as_view({"get": "list"})
        response = views(request)
        self.assertNotEqual(response.data["results"], [])
