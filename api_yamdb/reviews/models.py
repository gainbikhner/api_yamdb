from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from users.models import User


class Category(models.Model):
    """Категории (типы) произведений."""
    name = models.CharField('Категория', max_length=255)
    slug = models.SlugField('Адрес', max_length=50, unique=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField('Жанр', max_length=255)
    slug = models.SlugField('Адрес', max_length=50, unique=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""
    name = models.CharField('Произведение', max_length=256)
    year = models.PositiveSmallIntegerField('Год выхода')
    description = models.TextField('Описание', blank=True)
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
        through='GenreTitle',
        verbose_name='Жанр',
        related_name='genre'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
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


class GenreTitle(models.Model):
    """Модель для связывания."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Жанр и произведение'
        verbose_name_plural = 'Жанры и произведения'

    def __str__(self):
        return f'{self.title} и {self.genre}'


class Review(models.Model):
    """Отзывы."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Заголовок'
    )
    text = models.TextField('Текст')
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=[
            MinValueValidator(1, 'Не может быть меньше 1'),
            MaxValueValidator(10, 'Не может быть больше 10')
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
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
        related_name='comments',
        verbose_name='Произведение'
    )
    text = models.TextField('Комментарий')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
