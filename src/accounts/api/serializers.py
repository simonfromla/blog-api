from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
    )

User = get_user_model()

class UserCreateSerializer(ModelSerializer):
    # Override the default email field in order to allow custom validator,
    # and create custom email2 field
    email = EmailField(label="Email address")
    email2 = EmailField(label="Confirm Email")
    class Meta:
        model = User
        fields = [
        'username',
        'password',
        'email',
        'email2',
        ]
        extra_kwargs = {'password':
                            {'write_only':True}
                        }

    def validate(self, data):
    #     email = data['email']
    #     user_qs = User.objects.filter(email=email)
    #     if user_qs.exists():
    #         raise ValidationError('This user already exists')
        return data

    def validate_email(self, value):
        initial_data = self.get_initial()
        email1 = initial_data.get('email2')
        email2 = value

        #Validation to check whether username is already registered already exists,
        # but validation doesn't exist for email. Create custom validation
        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError('This user already exists')

        if email1 != email2:
            raise ValidationError('Emails must match')
        return value
    def validate_email2(self, value):
        initial_data = self.get_initial()
        email1 = initial_data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError('Emails must match')
        return value
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


class UserLoginSerializer(ModelSerializer):
    # Override the default email field in order to allow custom validator,
    # and create custom email2 field
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=False)
    email = EmailField(label="Email address", allow_blank=True, required=False)
    class Meta:
        model = User
        fields = [
        'username',
        'password',
        'email',
        'token',
        ]
        extra_kwargs = {'password':
                            {'write_only':True}
                        }

    def validate(self, data):
        user_obj = None
        email = data.get('email', None) # If email not present, default to None
        username = data.get('username', None)
        password = data['password']
        if not email and not username:
            raise ValidationError("A username or email is required to login.")

        user = User.objects.filter(
                    Q(email=email) |
                    Q(username=username)
                    ).distinct() # If two of the same model results, get one
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username or email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect password. Try Again.")

        data['token'] = "SOME_RANDOM_TOKEN"

        return data