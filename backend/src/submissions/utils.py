from submissions.models import Submission


def check_verdict(result, correct_output) -> Submission.Verdict:
    if result.returncode != 0:
        return Submission.Verdict.RE

    output = result.stdout.strip()

    if output == correct_output:
        return Submission.Verdict.AC
    else:
        return Submission.Verdict.WA
