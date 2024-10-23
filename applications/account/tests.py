from rest_framework.test import (
    APITestCase,
    force_authenticate,
    APIRequestFactory,
)
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from applications.account.views import (
    ChangePasswordAPIView,
    DeleteAccountAPIView,
)
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class UserRegisterTest(APITestCase):
    """Тесты для регистрации пользователя"""

    def setUp(self):
        self.url = reverse("register")
        self.User = get_user_model()

    def test_register_success(self):
        """Тест успешной регистрации пользователя"""
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
        """Тест ошибки при несовпадении паролей"""
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
        """Тест ошибки при неправильном формате email"""
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

    def test_password_length(self):
        """Тест ошибки при коротком пароле"""
        data = {
            "email": "testuser@gmail.com",
            "password": "a1",
            "password2": "a1",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAuthTests(APITestCase):
    """Тесты для аутентификации пользователя"""

    def setUp(self):
        self.email = "admin@gmail.com"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            email=self.email, password=self.password
        )

    def test_login_success(self):
        """Тест успешного входа пользователя"""
        url = reverse("login")
        response = self.client.post(
            url, {"email": self.email, "password": self.password}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_login_failure(self):
        """Тест ошибки при неправильном пароле"""
        url = reverse("login")
        response = self.client.post(
            url, {"email": self.email, "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserChangePasswordTests(APITestCase):
    """Тесты для смены пароля пользователя"""

    def setUp(self):
        self.email = "admin@gmail.com"
        self.password = "testpassword"
        self.new_password = "testpasswordnew"
        self.new_password_confirm = "testpasswordnew"
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email=self.email, password=self.password
        )

    def _login(self):
        url = reverse("login")
        response = self.client.post(
            url, {"email": self.email, "password": self.password}
        )
        return response

    def test_change_password(self):
        """Тест успешной смены пароля"""
        data = {
            "old_password": self.password,
            "new_password": self.new_password,
            "new_password_confirm": self.new_password_confirm,
        }
        url = reverse("change_password")
        request = self.factory.post(url, data, format="json")
        force_authenticate(request, self.user)
        view = ChangePasswordAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Вы успешно сменили пароль")
        self.assertEqual(
            self._login().status_code, status.HTTP_401_UNAUTHORIZED
        )


class UserDeleteTests(APITestCase):
    """Тесты для удаления аккаунта пользователя"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.email = "admin@gmail.com"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            email=self.email, password=self.password
        )
        self.data = {"email": self.email, "password": self.password}

    def test_delete_account(self):
        """Тест успешного удаления аккаунта"""
        url = reverse("delete-account")
        request = self.factory.delete(url, self.data, format="json")
        force_authenticate(request, self.user)
        view = DeleteAccountAPIView.as_view()
        response = view(request)
        self.assertEqual(response.data, "Аккаунт успешно удален.")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_account_password(self):
        """Тест пароля для удаления аккаунта"""
        url = reverse("delete-account")
        request = self.factory.delete(
            url, {"password": "testpassword0"}, format="json"
        )
        force_authenticate(request, self.user)
        view = DeleteAccountAPIView.as_view()
        response = view(request)
        self.assertEqual(
            response.data, "Неверный пароль для удаления аккаунта"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
