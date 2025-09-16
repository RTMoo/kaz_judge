from django.db import models
from datetime import datetime


def test_input_upload_path(instance, filename):
    """
    Генерирует путь для загрузки входного файла теста.
    """
    return f"problems_db/{instance.problem.id}/tests/input/{datetime.now()}.in"


def test_output_upload_path(instance, filename):
    """
    Генерирует путь для загрузки выходного файла теста.
    """
    return f"problems_db/{instance.problem.id}/tests/output/{filename}"


class Test(models.Model):
    input_file = models.FileField(
        upload_to=test_input_upload_path,
    )
    output_file = models.FileField(
        upload_to=test_output_upload_path,
        null=True,
        blank=True,
    )
    problem = models.ForeignKey(
        to="problems.Problem",
        on_delete=models.CASCADE,
        related_name="tests",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test {self.id} for problem {self.problem.id}"

    class Meta:
        ordering = ["created_at"]
