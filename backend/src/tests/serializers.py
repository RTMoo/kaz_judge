from rest_framework import serializers


class TestSerializer(serializers.Serializer):
    input_file = serializers.FileField()
    problem_id = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
