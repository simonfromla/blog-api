from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    )

from comments.models import Comment


class CommentCreateUpdateAPIView(ModelSerializer):
    class Meta:
        model = Comment
        fields =  [
            'content',
            'content_type',
            'parent',
            'id',
            'user',
            'object_id',
            ]

class CommentDetailSerializer(ModelSerializer):
    # user = SerializerMethodField()
    # image = SerializerMethodField()
    html = SerializerMethodField()

    class Meta:
        model = Comment
        fields =  [
            'content',
            'content_type',
            'parent',
            'id',
            'user',
            ]

    # def get_user(self, obj):
    #     return str(obj.user.username)
    # # def get_image(self, obj):
    # #     try:
    # #         image = obj.image.url
    # #     except:
    # #         image = None
    # #     return image
    # def get_html(self, obj):
    #     return obj.get_markdown()


class CommentListSerializer(ModelSerializer):
    # user = SerializerMethodField()
    class Meta:
        model = Comment
        fields =  [
            'content',
            'content_type',
            'parent',
            'id',
            'user',
            ]