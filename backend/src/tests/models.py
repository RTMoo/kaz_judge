from django.db import models


def test_input_upload_path(instance, filename):
    """
    Генерирует путь для загрузки входного файла теста.
    Пример: problems_db/{problem_id}/tests/{test_id}_input.txt
    """
    return f"problems_db/{instance.problem.id}/tests/{instance.id or 'tmp'}_input.txt"


class Test(models.Model):
    input_file = models.FileField(upload_to=test_input_upload_path)
    problem = models.ForeignKey(
        to="problems.Problem",
        on_delete=models.CASCADE,
        related_name="tests",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test {self.id} for problem {self.problem.id}"

    class Meta:
        ordering = ["-created_at"]
