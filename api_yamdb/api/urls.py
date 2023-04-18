from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUp, Token, UserMeView, UserViewSet


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', SignUp.as_view()),
    path('v1/auth/token/', Token.as_view()),
    path('v1/users/me/', UserMeView.as_view()),
    path('v1/', include(router_v1.urls)),
]
