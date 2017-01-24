from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    )

from comments.models import Comment


class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields =  [
            'content',
            'content_type',
            'parent',
            'id',
            'object_id',
            'reply_count',
            'timestamp',
            ]
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentChildSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields =  [
            'content',
            'id',
            'timestamp',
            ]

class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields =  [
            'content',
            'content_type',
            'id',
            'object_id',
            'reply_count',
            'replies',
            'timestamp',
            ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
