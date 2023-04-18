from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from .permissions import IsAdmin
from .serializers import (SignUpSerializer, TokenSerializer, UserMeSerializer,
                          UserSerializer)
from .utils import send_confirmation_code


class UserViewSet(ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username',)
    ordering = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')


class UserMeView(APIView):
    """Вью-функция для работы с текущим пользователем."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SignUp(APIView):
    """Вью-функция для регистрации и подтвержения по почте."""
    def post(self, request):
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).exists():
            send_confirmation_code(request)
            return Response(request.data, status=HTTP_200_OK)

        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_confirmation_code(request)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class Token(APIView):
    """Вью-функция для получения токена."""
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            user = get_object_or_404(User, username=username)
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
