from django.contrib import admin
from .models import *



class BlogThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_created', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_created')
    prepopulated_fields = {'slug': ('title',)}



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    # >,< coma is necessary bcz we pass tuple, it will be just str without ,
    # if more than 1 param , dont needed
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Blog_theme, BlogThemeAdmin)
admin.site.register(Category, CategoryAdmin)