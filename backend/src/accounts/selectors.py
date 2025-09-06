from accounts.models import CustomUser
from rest_framework.exceptions import NotFound


def get_user(**kwargs) -> CustomUser:
    """
    Возвращает пользователя по ключам.
    Args:
        **kwargs: Параметры фильтрации для поиска пользователя.
            Поддерживаются стандартные поля модели CustomUser
            (например, email="test@example.com", username="john").

    Returns:
        CustomUser: Объект пользователя.

    Raises:
        NotFound: Если пользователь не найден.
    """
    user = CustomUser.objects.filter(**kwargs).first()

    if not user:
        raise NotFound(detail="Пользователь не найден.")

    return user
