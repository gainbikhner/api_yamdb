from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from users.models import User


def send_confirmation_code(request):
    """Функция для получения кода подтверждения по почте."""
    user = get_object_or_404(User, username=request.data.get('username'))
    send_mail(
        'YaMDB. Confirmation code',
        f'confirmation_code: {default_token_generator.make_token(user)}',
        'access@yambd.ru',
        [user.email]
    )
