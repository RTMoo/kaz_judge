from tests.models import Test
from django.db.models import QuerySet



def get_problem_tests(problem_id: int) -> QuerySet[Test]:
    """
    Возвращает все тесты задачи.
    
    Args:
        problem_id (int): ID задачи.
    
    Returns:
        QuerySet: Все тесты задачи.
    """
    return Test.objects.filter(problem_id=problem_id)
