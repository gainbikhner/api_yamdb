from rest_framework.filters import BaseFilterBackend


class TitleFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        genre = request.query_params.get('genre')
        if genre:
            return queryset.filter(genre__slug=genre)

        category = request.query_params.get('category')
        if category:
            return queryset.filter(category__slug=category)

        year = request.query_params.get('year')
        if year:
            return queryset.filter(year=year)

        name = request.query_params.get('name')
        if name:
            return queryset.filter(name=name)

        return queryset
