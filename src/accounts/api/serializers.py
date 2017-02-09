from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
    )

User = get_user_model()

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
        'username',
        'password',
        'email',
        ]
        extra_kwargs = {'password':
                            {'write_only':True}
                        }
    def create(self, validated_data):
        print(validated_data)
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user_obj = User(
                        username=username,
                        email=email,
                        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data