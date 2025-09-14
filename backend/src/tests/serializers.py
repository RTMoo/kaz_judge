from rest_framework import serializers


class TestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    problem_id = serializers.IntegerField(read_only=True, source="problem.id")
    created_at = serializers.DateTimeField(read_only=True)
    preview = serializers.SerializerMethodField(read_only=True)
    input_file = serializers.FileField(write_only=True)

    def get_preview(self, obj):
        max_lines = 5
        try:
            with open(obj.input_file.path, "r") as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        break
                    lines.append(line.strip())
                return "\n".join(lines)
        except FileNotFoundError:
            return "[file missing]"
