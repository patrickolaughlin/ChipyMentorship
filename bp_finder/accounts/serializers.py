from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError
)

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            #  'first_name',
            #  'last_name',
        ]


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
        ]
        extra_kwargs = {"password": {"write_only": True}
                        }

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    email = EmailField(label='Email Address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',

        ]
        extra_kwargs = {"password":
                        {"write_only": True}
                        }

    def validate(self, data):
        #  user_obj = None
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        if not email and not username:
            raise ValidationError("A username and email is required to login")

        user = User.objects.filter(
            Q(email=email) | Q(username=username)
        ).distinct()
        # check for blank emails and exclude them
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials, please try again.")

        data["token"] = "SOME RANDOM TOKEN"

        return data
