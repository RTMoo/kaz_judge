from rest_framework import serializers


class SolutionSerializer(serializers.Serializer):
    solution = serializers.FileField()
