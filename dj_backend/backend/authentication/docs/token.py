from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

login_docs = extend_schema(
    summary="Obtain JWT token pair",
    description=(
        "Authenticate with username and password to receive a JWT access token "
        "and refresh token.\n\n"
        "- **access**: short-lived (60 min), attach as `Authorization: Bearer <token>`\n"
        "- **refresh**: long-lived (7 days), use at `/auth/token/refresh/` to rotate"
    ),
    tags=["Authentication"],
    request=TokenObtainPairSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenObtainPairSerializer,
            description="Token pair issued successfully",
            examples=[
                OpenApiExample(
                    "Success",
                    value={"access": "<jwt_access_token>", "refresh": "<jwt_refresh_token>"},
                )
            ],
        ),
        401: OpenApiResponse(description="Invalid credentials"),
    },
)

refresh_docs = extend_schema(
    summary="Rotate JWT access token",
    description=(
        "Exchange a valid refresh token for a new access token.\n\n"
        "With **ROTATE_REFRESH_TOKENS** enabled a new refresh token is also returned "
        "and the previous one is blacklisted immediately."
    ),
    tags=["Authentication"],
    request=TokenRefreshSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenRefreshSerializer,
            description="New token pair issued, old refresh token blacklisted",
            examples=[
                OpenApiExample(
                    "Success",
                    value={"access": "<new_jwt_access_token>", "refresh": "<new_jwt_refresh_token>"},
                )
            ],
        ),
        401: OpenApiResponse(description="Refresh token invalid or blacklisted"),
    },
)
