from rest_framework.serializers import ModelSerializer

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


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields =  [
            'title',
            'slug',
            'content',
            'publish',
            'id',
            ]


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields =  [
            'title',
            'slug',
            'content',
            'publish',
            'id',
            'user',
            ]


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