from django.urls import path
from . import views


urlpatterns = [
    path(
        "set-solution/",
        views.SetProblemSolutionView.as_view(),
        name="set_solution",
    ),
]
