import shutil
import subprocess
from pathlib import Path
from problems.models import Problem
from django.core.files.uploadedfile import InMemoryUploadedFile
from tests.selectors import get_problem_tests
from django.conf import settings
from rest_framework.exceptions import ValidationError


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


def clear_directory(path: Path) -> None:
    """Удаляет всё содержимое каталога, но оставляет сам каталог."""
    for item in path.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)


def compile_problem_outputs(problem: Problem) -> None:
    """
    Делает прогон по тестам с эталон решением и сохраняет ответ, предварительно очищая каталога outputs

    Args:
        problem (Problem): Задача

    Raises:
        ValidationError: Если нет тестов
        ValidationError: Если нет решения
    """
    tests = get_problem_tests(problem_id=problem.id)

    if len(tests) == 0:
        raise ValidationError(detail="Сначало добавьте тесты")

    output_dir = (
        Path(settings.MEDIA_ROOT) / "problems_db" / f"{problem.id}" / "tests" / "output"
    )

    clear_directory(output_dir)

    solution_path = Path(problem.solution.path)

    if not solution_path.exists():
        raise ValidationError(detail="Сначало загрузите решение")

    for ind, test in enumerate(tests, start=1):
        infile_path = Path(test.input_file.path)
        outfile_path = output_dir / f"{ind}.out"

        with open(infile_path, "r") as infile, open(outfile_path, "w") as outfile:
            subprocess.run(
                ["python3", solution_path],
                stdin=infile,
                stdout=outfile,
                stderr=subprocess.PIPE,
                text=True,
            )

        relative_path = outfile_path.relative_to(settings.MEDIA_ROOT)
        test.output_file.name = str(relative_path)
        test.save(update_fields=["output_file"])
