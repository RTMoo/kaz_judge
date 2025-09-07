from django.urls import path
from . import views


urlpatterns = [
    path("create/", views.CreateProblemView.as_view(), name="create_problem"),
    path("list/", views.ProblemListView.as_view(), name="problem_list"),
    path("<int:problem_id>/", views.ProblemDetailView.as_view(), name="problem_detail"),
    path(
        "<int:problem_id>/update/",
        views.UpdateProblemView.as_view(),
        name="update_problem",
    ),
    path(
        "<int:problem_id>/delete/",
        views.DeleteProblemView.as_view(),
        name="delete_problem",
    ),
]
