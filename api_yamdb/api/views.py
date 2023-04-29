from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .filters import TitleFilterBackend
from .mixins import (
    CreateListDestroyUpdateRetrieveViewSetMixin,
    CreateListDestroyViewSetMixin
)
from .permissions import IsAdmin, IsAdminOrSafeMethods, IsAuthor
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleRetrieveSerializer,
    TitleSerializer,
    TokenSerializer,
    UserMeSerializer,
    UserSerializer
)
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
    permission_classes = (AllowAny,)

    def post(self, request):
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).exists():
            send_confirmation_code(request)
            return Response(request.data, status=HTTP_200_OK)

        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(username=request.data.get('username'))
            send_confirmation_code(request)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class Token(APIView):
    """Вью-функция для получения токена."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            user = get_object_or_404(User, username=username)
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=HTTP_200_OK)
        return Response(
            {'confirmation_code': 'Неверный проверочный код.'},
            status=HTTP_400_BAD_REQUEST
        )


class CategoryViewSet(CreateListDestroyViewSetMixin):
    """Вьюсет для работы с категориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrSafeMethods,)


class GenreViewSet(CreateListDestroyViewSetMixin):
    """Вьюсет для работы с жанрами."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrSafeMethods,)


class TitleViewSet(CreateListDestroyUpdateRetrieveViewSetMixin):
    """Вьюсет для работы с произведениями."""
    queryset = Title.objects.all()
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('genre__slug',)
    filterset_class = TitleFilterBackend
    permission_classes = (IsAdminOrSafeMethods,)

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleRetrieveSerializer
        return TitleSerializer

    def get_queryset(self):
        new_queryset = Title.objects.annotate(rating=Avg('reviews__score'))
        return new_queryset.order_by('-id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = self.get_queryset().get(pk=serializer.instance.pk)
        serializer = TitleRetrieveSerializer(instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewViewSet(ModelViewSet):
    """Вьюсет для работы с отзывами."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all().order_by('-id')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        try:
            serializer.save(title=title, author=self.request.user)
        except IntegrityError:
            raise ValidationError(
                'Вы можете оставить только один отзыв на произведение.'
            )


class CommentViewSet(ModelViewSet):
    """Вьюсет для работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(title=title_id, review=review_id)
        return new_queryset.order_by('-id')

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(review=review, title=title, author=self.request.user)
