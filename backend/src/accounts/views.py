from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from accounts.utils import set_jwt_token
from accounts.models import CustomUser
from accounts import services
from accounts import serializers


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            if access_token and refresh_token:
                response = set_jwt_token(
                    response=response,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )
                # Удаляем токены из тела ответа
                del response.data["access"]
                del response.data["refresh"]

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.data["refresh"] = refresh_token

        try:
            response = super().post(request, *args, **kwargs)

            if response.status_code == status.HTTP_200_OK:
                new_access_token = response.data.get("access")

                if new_access_token:
                    response = set_jwt_token(
                        response=response, access_token=new_access_token
                    )
                    del response.data["access"]

            return response

        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User does not exist"}, status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomTokenBlacklistView(TokenBlacklistView):
    """
    Выход из системы и очистка куков
    """

    def post(self, request, *args, **kwargs):
        # Получаем refresh токен из куки (Потому что фронтенд не должен передавать вручную)
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Добавляем refresh-токен в данные запроса
        request.data.update({"refresh": refresh_token})

        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            # Удаляем куки с токенами
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

        return response


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.register_user(
            email=serializer.validated_data["email"],
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        return Response(status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.verify_email(
            email=serializer.validated_data["email"],
            code=serializer.validated_data["code"],
        )

        return Response(status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.change_password(
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
            current_user=request.user,
        )

        return Response(status=status.HTTP_200_OK)


class SendResetPasswordCodeView(APIView):
    serializer_class = serializers.SendResetPasswordCodeSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.send_reset_password_code(
            email=serializer.validated_data["email"],
        )

        return Response(status=status.HTTP_200_OK)


class VerifyResetPasswordCodeView(APIView):
    serializer_class = serializers.VerifyResetPasswordCodeSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.verify_reset_password_code(
            email=serializer.validated_data["email"],
            code=serializer.validated_data["code"],
            new_password=serializer.validated_data["new_password"],
        )

        return Response(status=status.HTTP_200_OK)
