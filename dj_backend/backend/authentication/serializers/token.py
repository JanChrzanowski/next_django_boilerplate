from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


class LoginSerializer(TokenObtainPairSerializer):
    pass


class RefreshSerializer(TokenRefreshSerializer):
    pass
