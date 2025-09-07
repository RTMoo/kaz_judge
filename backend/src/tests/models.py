from django.db import models
from .utils import test_input_upload_path


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
