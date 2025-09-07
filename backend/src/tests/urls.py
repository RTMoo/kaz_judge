from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateTestView.as_view(), name="create_test"),
    # path("list/", views.TestListView.as_view(), name="test_list"),
    # path("<int:test_id>/", views.TestDetailView.as_view(), name="test_detail"),
    # path("<int:test_id>/update/", views.UpdateTestView.as_view(), name="update_test"),
    # path("<int:test_id>/delete/", views.DeleteTestView.as_view(), name="delete_test"),
]
