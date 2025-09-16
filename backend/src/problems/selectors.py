from problems.models import Problem
from rest_framework.exceptions import NotFound
from django.db.models import QuerySet


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
    problem = Problem.objects.filter(**kwargs).select_related("author").first()

    if not problem:
        raise NotFound(detail="Задача не найдена.")

    return problem


def get_problems() -> QuerySet[Problem]:
    """
    Возвращает все задачи.
    """
    return Problem.objects.all().select_related("author")


def problem_exists_or_404(problem_id: int) -> None:
    """
    Если нет задачи вызовет исключение NotFound
    """
    if not Problem.objects.filter(id=problem_id).exists():
        raise NotFound(detail="Задача не найдена.")
