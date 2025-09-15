from django.urls import path
from . import views

urlpatterns = [
    path(
        "add/",
        views.AddTestView.as_view(),
        name="add_test/",
    ),
    path(
        "",
        views.ListTestView.as_view(),
        name="list_test",
    ),
    path(
        "<int:test_id>/delete/",
        views.DeleteTestView.as_view(),
        name="delete_test",
    ),
]
