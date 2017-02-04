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

from comments.models import Comment
from .serializers import (
    CommentDetailSerializer,
    CommentListSerializer,
    create_comment_serializer,
    )


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    # serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        slug = self.request.GET.get('slug')
        parent_id = self.request.GET.get('parent_id', None)
        return create_comment_serializer(
                model_type=model_type,
                slug=slug,
                parent_id=parent_id,
                user=self.request.user,
                )



# class CommentEditAPIView(RetrieveAPIView):
#     queryset = Comment.objects.all() # This '.all()' was changed by model manager to be only parent comments
#     serializer_class = CommentDetailSerializer
#     lookup_field = 'pk'
#     # lookup_url_kwarg = 'abc' # using 'slug' in the url vs. abc.
#     # def put(self, request, *args, **kwargs):
#     #     return self.update(request, *args, **kwargs)

class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0) # id__gte=0 will filter to be "true all"
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    #DRF built in search
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']

    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.filter(id__gte=0) #filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list
