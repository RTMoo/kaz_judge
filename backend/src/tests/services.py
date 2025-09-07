import zipfile
from tests.models import Test
from problems.models import Problem
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from rest_framework.exceptions import ValidationError
from django.core.files.base import ContentFile
from . import utils


ACCEPTED_EXTENSIONS = [".txt", ".zip"]


def create_test(
    input_file: InMemoryUploadedFile | TemporaryUploadedFile,
    problem: Problem,
) -> Test:
    ext = utils.get_file_suffix(input_file.name)

    if ext not in ACCEPTED_EXTENSIONS:
        raise ValidationError("Неподдерживаемое расширение файла.")

    if ext == ".txt":
        return Test.objects.create(
            input_file=input_file,
            problem=problem,
        )

    if ext == ".zip":
        created_tests = []

        with zipfile.ZipFile(input_file, "r") as archive:
            for file_name in archive.namelist():
                if file_name.startswith("__MACOSX/"):
                    continue
                
                if utils.get_file_suffix(file_name) != ".txt":
                    continue

                file_bytes = archive.read(file_name)

                # Джанговский тип файла
                django_file = ContentFile(
                    file_bytes,
                    name=file_name,
                )

                test = Test.objects.create(
                    input_file=django_file,
                    problem=problem,
                )
                created_tests.append(test)

        return created_tests
