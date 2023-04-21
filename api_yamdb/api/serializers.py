from rest_framework import serializers
import datetime

from reviews.models import Category, Genre_title, Genre, Titles, User


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
