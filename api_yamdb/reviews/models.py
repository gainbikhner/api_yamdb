from django.db import models
from django.core.validators import MaxLengthValidator


class Category(models.Model):
    """Категории (типы) произведений"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)


class Genre(models.Model):
    """Жанры произведений"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)


class Titles(models.Model):
    """Произведения"""
    name = models.CharField(
        max_length=256,
        validators=[MaxLengthValidator(256)]
    )
    year = models.IntegerField()
    # временная затычка
    rating = models.CharField(
        max_length=255,
        # on_delete=models.CASCADE,
        null=True,
        blank=True,)
    description = models.TextField(null=True, blank=True,)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        blank=True,
        related_name='category',)
    genre = models.ManyToManyField(
        Genre,
        # on_delete=models.SET_NULL,
        through='Genre_title',
        verbose_name='Жанр',
        # null=True,
        blank=True,
        related_name='genre'
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class User(models.Model):
    """Временный пользователь(затычка)"""
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Genre_title(models.Model):
    """Модель для связывания"""
    title_id = models.ForeignKey(Titles, on_delete=models.SET_NULL, null=True)
    genre_id = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.title_id} и {self.genre_id}'
