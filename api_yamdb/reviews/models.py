from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Category(models.Model):
    """Категории (типы) произведений."""
    name = models.CharField(max_length=255, verbose_name='Категория',)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Категория(slug)',
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(max_length=255, verbose_name='Жанр')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Жанр()slug'
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Произведение'
    )
    year = models.PositiveSmallIntegerField(verbose_name='Год выхода')
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        blank=True,
        related_name='category'
    )
    genre = models.ManyToManyField(
        Genre,
        through='Genretitle',
        verbose_name='Жанр',
        related_name='genre',
        blank=False
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__lte=timezone.now().year,),
                name='year_lte_current_year'
            ),
            models.CheckConstraint(
                check=models.Q(year__gte=0,),
                name='year_gte_minimum_year'
            ),
        ]

    def __str__(self):
        return self.name


class Genretitle(models.Model):
    """Модель для связывания."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} и {self.genre}'


class Review(models.Model):
    """Отзывы."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Не может быть меньше 1'),
            MaxValueValidator(10, 'Не может быть больше 10')
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text
