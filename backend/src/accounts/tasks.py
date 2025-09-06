from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_email(
    email: str,
    email_title: str,
    email_message: str,
) -> None:
    """
    Отправляет фоновое сообщение на указанный email.

    Args:
        email (str): Email адрес для отправки сообщения.
        email_title (str): Тема письма.
        email_message (str): Текст письма.
    """
    send_mail(
        subject=email_title,
        message=email_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
