import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import BlockedUser
from rest_framework.permissions import IsAdminUser
from .serializers import (
    ChangePasswordSerializers,
    DeleteAccountSerializer,
    RegisterSerializers,
    BlockedUserSerializer,
    UserListSerializer,
    UserDetailSerializer,
)

# получаем модель пользователя
User = get_user_model()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegisterAPIView(APIView):
    """
    Представление регистрации для модели Пользователя.

    Методы:
    -------
    post(request):
        Обрабатывает POST-запрос для регистрации нового пользователя.
        Проверяет валидность данных, сохраняет нового пользователя и логирует успешную регистрацию.
    """

    def post(self, request):
        """
        Обрабатывает POST-запрос для регистрации нового пользователя.

        Параметры:
        ----------
        request: Request
            HTTP-запрос, содержащий данные для регистрации.

        Возвращает:
        -----------
        Response
            HTTP-ответ с сообщением о успешной регистрации и статусом 201.
        """
        serializers = RegisterSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        logger.info(
            f"зарегистрирован новый  пользователь '{serializers.validated_data.get('email')}'"
        )
        return Response("Вы успешно зарегистрировались", status=201)


class DeleteAccountAPIView(APIView):
    """
    Представление удаления для модели Пользователя.

    Методы:
    -------
    delete(request):
        Обрабатывает DELETE-запрос для удаления  пользователя.
        Проверяет валидность данных, удаляет  пользователя и логирует успешное удаление.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """
        Обрабатывает DELETE-запрос для удаления  пользователя.

        Параметры:
        ----------
        request: Request
            HTTP-запрос, содержащий password для удаления пользователя.

        Возвращает:
        -----------
        Response
            HTTP-ответ с сообщением о успешном удалении и статусом 204.
        """
        user = request.user
        serializer = DeleteAccountSerializer(data=request.data)
        if serializer.is_valid():
            deletion_password = serializer.validated_data.get("password")

            if deletion_password and user.check_password(deletion_password):
                user.delete()
                logger.info(
                    f"Аккаунт пользователя '{request.user.email}' был успешно удален"
                )
                return Response(
                    "Аккаунт успешно удален.",
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                logger.info(
                    f"Неверный пароль для удаления аккаунта '{request.user.email}' "
                )
                return Response(
                    "Неверный пароль для удаления аккаунта",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordAPIView(APIView):
    """
    Представление Смены пароля для модели Пользователя ).

    Методы:
    -------
    post(request):
        Обрабатывает post-запрос для смены  пароля.
        Проверяет валидность данных, изменяет  пароль и логирует успешное
        изменение пароля.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Обрабатывает post-запрос для Смены пароля .

        Параметры:
        ----------
        request: Request
            HTTP-запрос, содержащий (
            password,
            new_password,
            new_password_confirm
            )
              для удаления пользователя.

        Возвращает:
        -----------
        Response
            HTTP-ответ с сообщением о успешной смене пароля  и статусом 200.
        """
        serializers = ChangePasswordSerializers(
            data=request.data, context={"request": request}
        )
        serializers.is_valid(raise_exception=True)
        serializers.set_new_password()
        logger.info(
            f"Пароль пользователя '{request.user.email}' был успешно изменён"
        )
        return Response("Вы успешно сменили пароль", status=200)


class BlockedUserViewSet(viewsets.ModelViewSet):
    """
    CRAD - Представление для для блокировке двух следующий функций
    1) создание постов
    2) доступ к приложению
    данно представление доступно только IsAdminUser
    принимает два boolean поля -> (can_create_posts, is_blocked)
    если ничего не передать по дефолту (отработат can_create_posts = False)
    """

    queryset = BlockedUser.objects.all()
    serializer_class = BlockedUserSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        logger.info(
            f"Админ {request.user} заблокировал  пользователя {response.data['id']}"
        )
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        logger.info(
            f"Админ {request.user} обновил данные блокировки пользователя {response.data['id']}"
        )
        return response

    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        response = super().destroy(request, *args, **kwargs)
        logger.info(
            f"Админ {request.user} удалил блокировку пользователя с ID {user_id}"
        )
        return response


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для для получения списка всех пользователей
    при детальном запросе, отображаться более
    развёрнутая информация
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        какой сериализатор будет использоватся ,
         зависит от запроса (get or get -> <int:id>)
        """
        if self.action == "list":
            return UserListSerializer
        if self.action == "retrieve":
            return UserDetailSerializer
        return super().get_serializer_class()
