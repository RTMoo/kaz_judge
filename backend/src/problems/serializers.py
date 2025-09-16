from rest_framework import serializers


class ProblemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    condition = serializers.CharField()
    author = serializers.CharField(source="author.username", read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
