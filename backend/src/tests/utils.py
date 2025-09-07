from pathlib import Path
from datetime import datetime
from uuid import uuid4


def test_input_upload_path(instance, filename):
    """
    Генерирует путь для загрузки входного файла теста.
    Пример: problems_db/{problem_id}/tests/{test_id}_input.txt
    """
    
    return f"problems_db/{instance.problem.id}/tests/{datetime.now()}_{uuid4().hex[:6]}_input.txt"


def get_file_suffix(
    file_name: str,
    many: bool = False,
) -> str | list[str]:
    """
    Возвращает расширение файла.

    Args:
        file_name (str): Имя файла.
        many (bool, optional): Если True, то возвращает список расширений. По умолчанию False.

    Returns:
        str | list[str]: Расширение файла.
    """
    if not many:
        return Path(file_name).suffix.lower()

    return [ext.lower() for ext in Path(file_name).suffixes]
