from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(max_length=9, choices=ROLES, default='user')
