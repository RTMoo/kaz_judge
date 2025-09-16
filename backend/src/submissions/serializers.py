from rest_framework import serializers
from submissions.models import Submission


class SubmissionSerializer(serializers.Serializer):
    submitted_file = serializers.FileField()
    verdict = serializers.ChoiceField(
        choices=Submission.Verdict.choices, read_only=True
    )
    problem_id = serializers.IntegerField(source="problem.id", read_only=True)
    sender = serializers.CharField(source="sender.username", read_only=True)
