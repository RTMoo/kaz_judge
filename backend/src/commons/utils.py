from pathlib import Path


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
