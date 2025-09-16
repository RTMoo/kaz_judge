from django.db import models
from commons.utils import get_file_suffix


def set_solution_path(
    instance,
    filename,
) -> str:
    """
    Генерирует путь для загрузки корректного решения.
    """
    ext = get_file_suffix(filename)
    new_filename = f"solution{ext}"

    return f"problems_db/{instance.id}/{new_filename}"


class Problem(models.Model):
    author = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
    )
    title = models.CharField(max_length=255)
    condition = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    solution = models.FileField(upload_to=set_solution_path, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
