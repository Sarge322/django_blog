from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class BlogThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_created', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_created')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'cat', 'content','get_html_photo', 'photo', 'is_published', 'time_created', 'time_updated')
    readonly_fields = ('time_created', 'time_updated', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'Миниатюра'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    # >,< coma is necessary bcz we pass tuple, it will be just str without ,
    # if more than 1 param , dont needed
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Blog_theme, BlogThemeAdmin)
admin.site.register(Category, CategoryAdmin)

# admin.site.site_title='Админ title'
# admin.site.site_header='Admins header'
