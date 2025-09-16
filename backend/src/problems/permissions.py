from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from problems.models import Problem


class IsProblemAuthor(BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view,
        obj: Problem,
    ) -> bool:
        return obj.author == request.user
