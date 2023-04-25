from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    SignUp,
    TitleViewSet,
    Token,
    UserMeView,
    UserViewSet
)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', SignUp.as_view()),
    path('v1/auth/token/', Token.as_view()),
    path('v1/users/me/', UserMeView.as_view()),
    path('v1/', include(router_v1.urls)),
]
