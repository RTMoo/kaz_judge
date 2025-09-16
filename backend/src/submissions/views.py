from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.request import Request
from . import serializers
from . import services
from problems.selectors import get_problem


class SubmitSolutionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SubmissionSerializer

    def post(self, request: Request, problem_id: int):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        problem = get_problem(id=problem_id)

        submission = services.submit_solution(
            problem=problem,
            solution=serializer.validated_data["submitted_file"],
            sender=request.user,
        )
        data = self.serializer_class(submission).data

        return Response(
            status=status.HTTP_201_CREATED,
            data=data,
        )
