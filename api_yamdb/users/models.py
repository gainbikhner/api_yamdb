from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    """Кастомная модель пользователя."""
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=15,
        choices=ROLES,
        default='user'
    )
    email = models.EmailField(
        'Почта',
        unique=True,
        error_messages={
            'unique': 'Пользователь с такой почтой уже существует.'
        }
    )
