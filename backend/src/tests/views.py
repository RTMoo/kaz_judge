from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import serializers
from . import services
from . import selectors
from problems.selectors import get_problem, problem_exists_or_404


class CreateTestView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.TestSerializer

    def post(self, request: Request, problem_id: int):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        problem = get_problem(id=problem_id)
        test = services.create_test(
            input_file=serializer.validated_data["input_file"],
            problem=problem,
        )

        data = self.serializer_class(test, many=True).data

        return Response(status=status.HTTP_201_CREATED, data=data)


class ListTestView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.TestSerializer

    def get(self, request: Request, problem_id: int):
        problem_exists_or_404(problem_id=problem_id)
        tests = selectors.get_problem_tests(problem_id=problem_id)

        data = self.serializer_class(tests, many=True).data

        return Response(status=status.HTTP_200_OK, data=data)
        