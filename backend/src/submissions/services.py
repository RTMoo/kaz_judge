import subprocess
import tempfile
from problems.models import Problem
from django.core.files.uploadedfile import InMemoryUploadedFile
from accounts.models import CustomUser
from tests.selectors import get_problem_tests
from submissions.models import Submission
from submissions.utils import check_verdict


def submit_solution(
    problem: Problem,
    solution: InMemoryUploadedFile,
    sender: CustomUser,
) -> Submission:
    tests = get_problem_tests(problem_id=problem.id)

    submission = Submission.objects.create(
        sender=sender,
        problem=problem,
        verdict=Submission.Verdict.AC,
        submitted_file=solution,
    )

    submitted_file = submission.submitted_file.path

    for test in tests:
        correct_output_path = test.output_file.path
        infile_path = test.input_file.path

        with open(correct_output_path, "r") as f:
            correct_output = f.read().strip()

        with open(infile_path, "r") as infile:
            result = subprocess.run(
                ["python3", submitted_file],
                stdin=infile,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

        verdict = check_verdict(
            result=result,
            correct_output=correct_output,
        )

        if verdict != Submission.Verdict.AC:
            submission.verdict = verdict
            submission.save(update_fields=["verdict"])
            return submission

    return submission
