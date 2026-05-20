from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ..docs.token import login_docs, refresh_docs
from ..serializers import LoginSerializer, RefreshSerializer


@login_docs
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


@refresh_docs
class RefreshView(TokenRefreshView):
    serializer_class = RefreshSerializer
