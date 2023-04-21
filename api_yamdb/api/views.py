from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Genre_title, Titles, User
from .filters import TitlesFilterBackend
from .mixins import (CreateListDestroyUpdateRetrieveViewSetMixin,
                     CreateListDestroyViewSetMixin)
from .serializers import (CategorySerializer, Genre_titleSerializer,
                          GenreSerializer, TitlesSerializer,
                          TitlesSerializerRetrieve, UserSerializer)


class CategoryViewSet(CreateListDestroyViewSetMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSetMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class Genre_titleViewSet(viewsets.ModelViewSet):
    queryset = Genre_title.objects.all()
    serializer_class = Genre_titleSerializer


class TitleViewSet(CreateListDestroyUpdateRetrieveViewSetMixin):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, TitlesFilterBackend,)
    search_fields = ('genre__slug',)
    filterset_fields = ('genre', 'category', 'year', 'name')

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitlesSerializerRetrieve
        return TitlesSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
