from rest_framework import serializers


class TestSerializer(serializers.Serializer):
    input_file = serializers.FileField()
    created_at = serializers.DateTimeField(read_only=True)
