from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .token import account_activation_token
from reward.serializer import FundingSerializer, ProductLikeSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        max_length=12, min_length=1, allow_blank=False, write_only=True)
    nickname = serializers.CharField(
        max_length=20, validators=[UniqueValidator(queryset=User.objects.all())])
    funding_set = FundingSerializer(many=True, required=False)
    like_products = ProductLikeSerializer(many=True, required=False)

    class Meta:
        model = User

        fields = (
            'pk',
            'username',
            'password',
            'nickname',
            'img_profile',
            'like_products',
            'funding_set'
        )

    def validate_password(self, value):
        if value == self.initial_data.get('check_password'):
            return value
        raise ValidationError('(password, check_password) 불일치')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
        )
        user.is_active = False
        user.save()

        message = render_to_string('user/account_activate_email.html', {
            'user': user,
            'domain': 'ryanden.kr',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
            'token': account_activation_token.make_token(user),
        })

        mail_subject = 'test'
        to_email = user.username
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return validated_data


class UserChangeInfoSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], required=False)
    password = serializers.CharField(
        required=True, max_length=12, min_length=1, write_only=True)
    nickname = serializers.CharField(
        max_length=20, validators=[UniqueValidator(queryset=User.objects.all())], required=False)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password',
            'nickname',
            'img_profile',
        )

    def validate_password(self, value):
        if self.instance.check_password(self.initial_data.get('password')):
            return value
        raise ValidationError('password 가 틀렸습니다')

    def validate(self, data):
        if self.initial_data.get('new_password'):
            if self.initial_data.get('new_password') == self.initial_data.get('check_password'):
                data['password'] = make_password(self.initial_data.get('new_password'))
            else:
                raise ValidationError('(new_password, check_password) 불일치')
        else:
            data['password'] = make_password(self.initial_data.get('password'))
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'nickname',
            'img_profile',
        )


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'password',
        )

    def validate_password(self, value):
        if self.instance.check_password(value):
            value
            return value
        raise ValidationError('password 가 틀렸습니다')
