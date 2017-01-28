from comments.api.serializers import CommentSerializer
from comments.models import Comment

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    )

from posts.models import Post


class PostCreateUpdateAPIView(ModelSerializer):
    class Meta:
        model = Post
        fields =  [
            'title',
            # 'slug',
            'content',
            'publish',
            # 'id',
            ]

post_detail_url = HyperlinkedIdentityField(
        view_name = 'posts-api:detail',
        lookup_field = 'slug'
        )

class PostDetailSerializer(ModelSerializer):
    comments =SerializerMethodField()
    url = post_detail_url
    user = SerializerMethodField()
    # image = SerializerMethodField()
    html = SerializerMethodField()

    class Meta:
        model = Post
        fields =  [
            'url',
            'image',
            'title',
            'content',
            'html',
            'publish',
            'id',
            'user',
            'comments',
            ]

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments

    def get_user(self, obj):
        return str(obj.user.username)
    # def get_image(self, obj):
    #     try:
    #         image = obj.image.url
    #     except:
    #         image = None
    #     return image
    def get_html(self, obj):
        return obj.get_markdown()


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = SerializerMethodField()
    class Meta:
        model = Post
        fields =  [
            'url',
            'title',
            'slug',
            'content',
            'publish',
            'id',
            'user',
            ]
    def get_user(self, obj):
        return str(obj.user.username)


"""
from posts.models import Post
from posts.api.serializers import PostDetailSerializer

data = {
    'title': "yeahh buddy",
    'content': "new content",
    'publish': "2016-2-12",
    'slug': 'yeah-buddy',
}

obj = Post.objects.get(id=2)
new_item = PostDetailSerializer(obj, data=data)


[description]
"""