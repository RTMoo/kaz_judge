from django.db import models
from datetime import datetime
from tests.utils import get_file_suffix


def submit_file_upload_path(
    instance,
    filename,
) -> str:
    now = datetime.now()
    ext = get_file_suffix(filename)
    new_filename = f"{now.strftime('%H-%M-%S-%f')}_user_{instance.sender.username}_problem_{instance.problem_id}{ext}"

    return f"submissions/{now.strftime('%Y/%m/%d')}/{new_filename}"


class Submission(models.Model):
    class Verdict(models.TextChoices):
        AC = "AC", "Accepted"
        WA = "WA", "Wrong Answer"
        TLE = "TLE", "Time Limit Exceeded"
        RE = "RE", "Runtime Error"
        CE = "CE", "Compilation Error"

    sender = models.ForeignKey(
        to="accounts.CustomUser",
        on_delete=models.CASCADE,
    )
    submitted_file = models.FileField(
        upload_to=submit_file_upload_path,
    )
    problem = models.ForeignKey(
        to="problems.Problem",
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    verdict = models.CharField(
        choices=Verdict.choices,
        max_length=3,
        default=Verdict.WA,
    )
    created_at = models.DateTimeField(auto_now_add=True)
