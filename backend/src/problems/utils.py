import shutil
from pathlib import Path
from problems.models import Problem
from django.conf import settings


def create_directory(path: Path) -> None:
    """Создает директорию с указанным путем."""
    path.mkdir(parents=True, exist_ok=True)


def create_problem_dir_structure(problem: Problem) -> None:
    """Создает директории для задачи."""
    dir_path = (
        Path(settings.MEDIA_ROOT)
        / "problems_db"
        / f"{problem.id}"
    )

    create_directory(dir_path)
    create_directory(dir_path / "tests" / "input")
    create_directory(dir_path / "tests" / "output")


def remove_problem_dir_structure(problem: Problem) -> None:
    """Удаляет директории для задачи."""
    dir_path = (
        Path(settings.MEDIA_ROOT)
        / "problems_db"
        / f"{problem.id}"
    )

    try:
        shutil.rmtree(dir_path)
    except FileNotFoundError:
        print(f"Directory {dir_path} not found")
