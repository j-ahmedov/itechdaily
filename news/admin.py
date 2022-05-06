from django.contrib import admin
from .models import News, Category


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'updated_date', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ['id']


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
