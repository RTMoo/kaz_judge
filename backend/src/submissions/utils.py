from submissions.models import Submission
from django.core.files.uploadedfile import InMemoryUploadedFile


def check_verdict(result, correct_output) -> Submission.Verdict:
    if result.returncode != 0:
        return Submission.Verdict.RE

    output = result.stdout.strip()

    if output == correct_output:
        return Submission.Verdict.AC
    else:
        return Submission.Verdict.WA


def get_file_text(file: InMemoryUploadedFile) -> str:
    file.seek(0)
    content = file.read()
    return content.decode()
