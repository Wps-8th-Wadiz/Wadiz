import traceback

from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework import generics, status, permissions

from members.token import account_activation_token
from ..serializer import UserSerializer, UserChangeInfoSerializer, UserDetailSerializer, UserDeleteSerializer

User = get_user_model()


class UserList(APIView):

    def get(self, request):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get(self, request, pk):
        serializer = UserDetailSerializer(User.objects.get(pk=pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    permissions = (permissions.IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        serializer = UserChangeInfoSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = User.objects.get(username=request.user)
        serializer = UserDeleteSerializer(user, data=request.data)
        if serializer.is_valid():
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class AuthToken(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, __ = Token.objects.get_or_create(user=user)

            data = {
                'token': token.key,
            }
            return Response(data)
        raise AuthenticationFailed('인증정보가 올바르지 않습니다')


class UserActivate(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return Response(user.email + '계정이 활성화 되었습니다', status=status.HTTP_200_OK)
            else:
                return Response('만료된 링크입니다', status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(traceback.format_exc())


class UserInfo(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(username=request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data, HTTP_200_OK)
