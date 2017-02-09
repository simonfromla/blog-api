from django.contrib.auth import get_user_model

from django.db.models import Q
from rest_framework.filters import (
    SearchFilter, OrderingFilter
    )
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )

from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

from posts.api.permissions import IsOwnerOrReadOnly

from .serializers import (
    UserCreateSerializer,
    )

User = get_user_model()

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


