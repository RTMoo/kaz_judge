from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.request import Request
from problems.selectors import get_problem
from . import serializers
from . import services


class SetProblemSolutionView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.SolutionSerializer

    def post(self, request: Request, problem_id: int):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        problem = get_problem(id=problem_id)
        services.set_problem_solution(
            problem=problem,
            solution=serializer.validated_data["solution"],
        )

        return Response(status=status.HTTP_201_CREATED)


class CompileProblemOutputsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request: Request, problem_id: int):
        problem = get_problem(id=problem_id)
        services.compile_problem_outputs(
            problem=problem,
        )

        return Response(status=status.HTTP_200_OK)
