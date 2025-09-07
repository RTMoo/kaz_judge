from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.request import Request
from problems import serializers
from problems import services
from problems import utils
from problems import selectors


class CreateProblemView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.ProblemSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        problem = services.create_problem(
            title=serializer.validated_data["title"],
            condition=serializer.validated_data["condition"],
        )

        utils.create_problem_dir_structure(problem=problem)

        data = self.serializer_class(problem).data

        return Response(status=status.HTTP_201_CREATED, data=data)


class ProblemDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ProblemSerializer

    def get(self, request: Request, problem_id: int):
        problem = selectors.get_problem(id=problem_id)
        data = self.serializer_class(problem).data

        return Response(status=status.HTTP_200_OK, data=data)


class ProblemListView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ProblemSerializer

    def get(self, request: Request):
        problems = selectors.get_problems()
        data = self.serializer_class(problems, many=True).data

        return Response(status=status.HTTP_200_OK, data=data)


class UpdateProblemView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.ProblemSerializer

    def patch(self, request: Request, problem_id: int):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        problem = selectors.get_problem(id=problem_id)
        problem = services.update_problem(
            problem=problem,
            title=serializer.validated_data["title"],
            condition=serializer.validated_data["condition"],
        )

        data = self.serializer_class(problem).data

        return Response(status=status.HTTP_200_OK, data=data)


class DeleteProblemView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request: Request, problem_id: int):
        problem = selectors.get_problem(id=problem_id)
        services.delete_problem(problem=problem)

        return Response(status=status.HTTP_204_NO_CONTENT)
