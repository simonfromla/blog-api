from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    )

from comments.models import Comment


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields =  [
            'content',
            'content_type',
            'parent',
            'id',
            'object_id',
            ]
