from problems.models import Problem
from django.core.files.uploadedfile import InMemoryUploadedFile


def set_problem_solution(
    problem: Problem,
    solution: InMemoryUploadedFile,
) -> None:
    """
    Устанавливает код решения задачи. Если ранее был код решения, он удаляется.

    Args:
        problem (Problem): Задача.
        solution (InMemoryUploadedFile): Код решения.
    """
    if problem.solution:
        problem.solution.delete(save=False)

    problem.solution = solution
    problem.save()
