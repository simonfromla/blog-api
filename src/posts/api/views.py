from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    )

from posts.models import Post
from .serializers import (
    PostCreateUpdateAPIView,
    PostDetailSerializer,
    PostListSerializer,
    )


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateAPIView


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    lookup_field = 'slug'

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    # lookup_url_kwarg = 'abc' # using 'slug' in the url vs. abc.

class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateAPIView
    lookup_field = 'slug'
