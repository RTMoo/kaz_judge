from tests.models import Test
from django.db.models import QuerySet
from rest_framework.exceptions import NotFound, ValidationError


def get_problem_tests(problem_id: int) -> QuerySet[Test]:
    """
    Возвращает все тесты задачи.

    Args:
        problem_id (int): ID задачи.

    Returns:
        QuerySet: Все тесты задачи.
    """
    return Test.objects.filter(problem_id=problem_id)


def get_problem_test(problem_id: int, test_id: int) -> Test:
    """
    Возвращает тест задачи.

    Args:
        problem_id (int): ID задачи.
        test_id (int): ID теста.

    Returns:
        Test: Тест задачи.
    """
    test = Test.objects.filter(id=test_id, problem_id=problem_id).first()

    if not test:
        raise NotFound("Тест не найден.")

    return test
