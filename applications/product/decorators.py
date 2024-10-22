from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def rating_schema():
    return swagger_auto_schema(
        methods=["post"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "rating_change": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["increase", "decrease"],
                    description="Увеличить или уменьшить рейтинг поста",
                )
            },
            required=["rating_change"],
        ),
        responses={
            200: openapi.Response(
                description="Успешное изменение рейтинга",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "new_rating": openapi.Schema(
                            type=openapi.TYPE_INTEGER
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="Недопустимое значение rating_change",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
