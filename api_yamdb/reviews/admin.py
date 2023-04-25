from django.contrib import admin

from .models import Category, Genre_title, Genre, Title, Review, Comment


# class ReviewsAdmin(admin.ModelAdmin):
#    list_display = ('pk', 'text', 'pub_date', 'author', 'group',)
#    search_fields = ('text',)
#    list_editable = ('group',)
#    list_filter = ('pub_date',)
#    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Genre_title)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
