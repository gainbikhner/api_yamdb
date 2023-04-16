from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SignUp, Token

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', SignUp.as_view()),
    path('v1/auth/token/', Token.as_view()),
    path('v1/', include(router_v1.urls)),
]
