from django.urls import path
from . import views

urlpatterns = [
    path(
        "register/",
        views.RegistrationView.as_view(),
        name="register",
    ),
    path(
        "login/",
        views.LoginView.as_view(),
        name="login",
    ),
    path(
        "refresh/",
        views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "logout/",
        views.CustomTokenBlacklistView.as_view(),
        name="logout",
    ),
    path(
        "verify_email/",
        views.VerifyEmailView.as_view(),
        name="verify_email",
    ),
    path(
        "change_password/",
        views.ChangePasswordView.as_view(),
        name="change_password",
    ),
    path(
        "reset_password/",
        views.SendResetPasswordCodeView.as_view(),
        name="reset_password",
    ),
    path(
        "verify_reset_password/",
        views.VerifyResetPasswordCodeView.as_view(),
        name="verify_reset_password",
    ),
]
