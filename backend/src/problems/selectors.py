from problems.models import Problem
from rest_framework.exceptions import NotFound


def get_problem(**kwargs) -> Problem:
    """
    Возвращает задачу по фильтрам или NotFound.

    Args:
        **kwargs: Поля фильтрации модели Problem.

    Returns:
        Problem: Найденная задача.

    Raises:
        NotFound: Если задача не найдена.
    """
    problem = Problem.objects.filter(**kwargs).first()

    if not problem:
        raise NotFound(detail="Задача не найдена.")

    return problem


def get_problems() -> list[Problem]:
    """
    Возвращает все задачи.
    """
    return Problem.objects.all()
