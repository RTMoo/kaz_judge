from django.urls import path
from . import views


urlpatterns = [
    path(
        "submit/",
        views.SubmitSolutionView.as_view(),
        name="submit",
    )
]
