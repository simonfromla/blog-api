from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

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
    url = post_detail_url
    class Meta:
        model = Post
        fields =  [
            'url',
            'title',
            'content',
            'publish',
            'id',
            ]


class PostListSerializer(ModelSerializer):
    url = post_detail_url
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