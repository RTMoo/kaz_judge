from django.conf import settings
from rest_framework.response import Response
from random import randint


def set_jwt_token(
    response: Response,
    access_token: str,
    refresh_token: str | None = None,
) -> Response:
    """
    Устанавливает access и refresh токены в куки ответа.

    Args:
        response (Response): Исходный HTTP-ответ.
        access_token (str): Access JWT токен.
        refresh_token (Optional[str], optional): Refresh JWT токен. По умолчанию None.

    Returns:
        Response: HTTP-ответ с установленными куки.
    """
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE", False),
        samesite=settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE", "Lax"),
        max_age=settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME").total_seconds(),
    )

    if refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE", False),
            samesite=settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE", "Lax"),
            max_age=settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME").total_seconds(),
        )

    return response


def generate_code(length: int = 6) -> str:
    """
    Генерирует случайное число с длиной length.

    Args:
        length (int, optional): Длина генерируемого числа. По умолчанию 6.

    Returns:
        str: Сгенерированное число.
    """
    return "".join([str(randint(0, 9)) for _ in range(length)])
