from django.contrib import admin
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'description', 'publish', 'status')
    list_filter = ('status', 'date', 'publish', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)


class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "parent", "id")
    mptt_level_indent = 20
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "parent")
    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
    )


admin.site.register(Category, CategoryAdmin)
