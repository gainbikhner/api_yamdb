from django.db import models
from django.core.validators import (MaxLengthValidator, 
                                    MinValueValidator, MaxValueValidator)
from users.models import User


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


class Genre_title(models.Model):
    """Модель для связывания"""
    title_id = models.ForeignKey(Titles, on_delete=models.SET_NULL, null=True)
    genre_id = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.title_id} и {self.genre_id}'


class Review(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, 'Не может быть меньше 1'),
                    MaxValueValidator(10, 'Не может быть больше 10')])
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='title_author')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)