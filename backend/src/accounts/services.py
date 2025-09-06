from django.core.cache import cache
from rest_framework.exceptions import ValidationError, NotFound
from accounts.models import CustomUser
from accounts.tasks import send_email
from accounts.selectors import get_user
from accounts.utils import generate_code
# from profiles.services import create_profile


def register_user(
    email: str,
    username: str,
    password: str,
) -> None:
    """
    Регистрирует нового пользователя или обновляет существующего.

    Args:
        email (str): Почта пользователя.
        username (str): Имя пользователя.
        password (str): Пароль пользователя.

    Raises:
        ValidationError: Если email уже используется подтвержденным пользователем.
    """
    user = get_user(email=email)
    if user:
        if user.email_verified:
            raise ValidationError(detail="Этот email уже используется")

        # Обновить данные, если пользователь неактивен
        user.username = username
        user.set_password(password)
        user.save()
    else:
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

    code = generate_code()

    timeout_minutes = 5
    cache.set(email, code, timeout_minutes * 60)

    send_email.delay(
        email=user.email,
        email_title="Верификация почты",
        email_message=f"Код верификации: {code}, время действия кода {timeout_minutes} минут",
    )

    return None


def verify_email(email: str, code: str) -> None:
    """
    Подтверждает email пользователя по коду.

    Args:
        email (str): Email пользователя.
        code (str): Код подтверждения.

    Raises:
        NotFound: Если пользователь не найден.
        ValidationError: Если почта уже подтверждена, код истек или неверный.
    """
    user = get_user(email=email)

    if not user:
        raise NotFound(detail="Пользователь не найден")

    if user.email_verified:
        raise ValidationError(detail="Почта уже подтверждена")

    real_code = cache.get(email)

    if real_code is None:
        raise ValidationError(
            detail="Код истёк или не запрашивался",
        )

    if code != real_code:
        raise ValidationError(detail="Неверный код")

    user.email_verified = True
    user.save()

    # create_profile(user)
    cache.delete(email)


def change_password(
    old_password: str,
    new_password: str,
    current_user: CustomUser,
) -> None:
    """
    Изменяет пароль пользователя.

    Args:
        old_password (str): Старый пароль пользователя.
        new_password (str): Новый пароль пользователя.
        current_user (CustomUser): Объект пользователя.

    Raises:
        ValidationError: Если новый пароль совпадает со старым.
        ValidationError: Если старый пароль неверный.
    """
    if old_password == new_password:
        raise ValidationError(detail="Новый пароль не должен совпадать со старым")

    if not current_user.check_password(old_password):
        raise ValidationError(
            detail="Неправильный пароль, попробуйте еще раз или сбросьте пароль"
        )

    current_user.set_password(new_password)
    current_user.save()


def send_reset_password_code(email: str) -> None:
    """
    Сбрасывает пароль пользователя.

    Args:
        email (str): Почта пользователя.

    Raises:
        ValidationError: Если пользователь не активен.
    """
    user = get_user(email=email)

    code = generate_code()

    timeout_minutes = 5
    cache.set(email, code, timeout_minutes * 60)

    send_email.delay(
        email=user.email,
        email_title="Сброс пароля",
        email_message=f"Код сброса пароля: {code}, время действия кода {timeout_minutes} минут",
    )


def verify_reset_password_code(
    email: str,
    code: str,
    new_password: str,
) -> None:
    """
    Проверяет код сброса пароля и меняет пароль.

    Args:
        email (str): Email пользователя.
        code (str): Код сброса пароля.
        new_password (str): Новый пароль пользователя.
    """
    user = get_user(email=email)

    real_code = cache.get(email)

    if real_code is None:
        raise ValidationError(detail="Код истёк или не запрашивался")

    if code != real_code:
        raise ValidationError(detail="Неверный код")

    user.set_password(new_password)
    user.save()

    cache.delete(email)
