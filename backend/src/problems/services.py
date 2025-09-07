from problems.models import Problem
from problems import utils


def create_problem(
    title: str,
    condition: str,
) -> Problem:
    """
    Создает задачу.

    Args:
        title (str): Заголовок задачи.
        condition (str): Условие задачи.

    Returns:
        Problem: Созданная задача.
    """
    return Problem.objects.create(
        title=title,
        condition=condition,
    )


def update_problem(
    problem: Problem,
    title: str,
    condition: str,
) -> Problem:
    """
    Обновляет поля задачи.

    Args:
        problem_id (int): ID задачи.
        title (str|None): Новый заголовок.
        condition (str|None): Новое условие.

    Returns:
        Problem: Обновленная задача.

    Raises:
        ValidationError: Если нет данных для обновления.
    """

    problem.title = title
    problem.condition = condition
    problem.save()

    return problem


def delete_problem(problem: Problem) -> None:
    """
    Удаляет задачу.

    Args:
        problem (Problem): Удаляемая задача.

    Returns:
        None
    """

    utils.remove_problem_dir_structure(problem=problem)
    problem.delete()
