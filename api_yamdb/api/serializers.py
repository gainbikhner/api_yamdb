from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from reviews.models import Category, Genre_title, Genre, Titles
from users.models import User
import datetime
from rest_framework.validators import UniqueTogetherValidator

from review.models import Comment, Review


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class UserMeSerializer(UserSerializer):
    """Сериализатор для текущего пользователя."""
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Использовать имя _me_ в качестве username запрещено."
            )

    class Meta:
        fields = ('email', 'username')
        model = User


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        confirmation_code = data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            return data
        raise serializers.ValidationError('Неверный проверочный код.')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class Genre_titleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre_title
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializerRetrieve(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError("Год не может быть в будущем")
        return value

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'The length of the name field must be 256 characters or less.'
            )
        return value

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('title', 'text', 'score', 'author', 'created')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('title', 'review')
        model = Comment
