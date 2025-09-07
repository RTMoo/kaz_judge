import shutil
from pathlib import Path
from problems.models import Problem
from slugify import slugify


def create_directory(path: Path) -> None:
    """Создает директорию с указанным путем."""
    path.mkdir(parents=True, exist_ok=True)


def create_problem_dir_structure(problem: Problem) -> None:
    """Создает директории для задачи."""
    dir_path = (
        Path(__file__).resolve().parent.parent
        / "problems_db"
        / f"{problem.id}-{slugify(problem.title)}"
    )

    create_directory(dir_path)
    create_directory(dir_path / "tests")
    create_directory(dir_path / "solutions")


def remove_problem_dir_structure(problem: Problem) -> None:
    """Удаляет директории для задачи."""
    dir_path = (
        Path(__file__).resolve().parent.parent
        / "problems_db"
        / f"{problem.id}-{slugify(problem.title)}"
    )

    try:
        shutil.rmtree(dir_path)
    except FileNotFoundError:
        print(f"Directory {dir_path} not found")
