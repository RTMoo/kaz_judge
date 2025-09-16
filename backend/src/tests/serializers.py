from rest_framework import serializers
from tests.utils import get_file_preview
from tests.models import Test


class TestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    problem_id = serializers.IntegerField(read_only=True, source="problem.id")
    created_at = serializers.DateTimeField(read_only=True)
    input_preview = serializers.SerializerMethodField(read_only=True)
    output_preview = serializers.SerializerMethodField(read_only=True)
    input_file = serializers.FileField(write_only=True)

    def get_input_preview(self, obj: Test):
        get_file_preview(file_path=obj.input_file.path, max_lines=5)

    def get_output_preview(self, obj: Test):
        get_file_preview(file_path=obj.output_file.path, max_lines=5)
