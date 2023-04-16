from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response

from users.models import User
from .serializers import UserSerializer, SignUpSerializer, TokenSerializer
from .permissions import IsNotMe


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignUp(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsNotMe,)

    def post(self, request):
        response = self.create(request)
        user = get_object_or_404(User, username=request.data.get('username'))
        send_mail(
            'YaMDB. Confirmation code',
            f'confirmation_code: {default_token_generator.make_token(user)}',
            'access@yambd.ru',
            [user.email]
        )
        return response


class Token(CreateAPIView):
    serializer_class = TokenSerializer

    def post(self, request):
        user = get_object_or_404(User, username=request.data.get('username'))
        confirmation_code = request.data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)})
