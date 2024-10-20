import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import (
    ChangePasswordSerializers,
    DeleteAccountSerializer,
    RegisterSerializers,
)


User = get_user_model()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegisterAPIView(APIView):

    def post(self, request):
        serializers = RegisterSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()

        logger.info(
            f"зарегистрирован новый  пользователь '{serializers.validated_data.get('email')}'"
        )
        return Response("Вы успешно зарегистрировались", status=201)


class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
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
                    "Неверный пароль для удаления аккаунта.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializers(
            data=request.data, context={"request": request}
        )
        serializers.is_valid(raise_exception=True)
        serializers.set_new_password()
        logger.info(
            f"Пароль пользователя '{request.user.email}' был успешно изменён"
        )
        return Response("Вы успешно сменили пароль", status=200)
