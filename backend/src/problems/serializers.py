from rest_framework import serializers


class ProblemSerializer(serializers.Serializer):
    title = serializers.CharField()
    condition = serializers.CharField()
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
