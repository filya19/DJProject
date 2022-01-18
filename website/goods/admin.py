from django.contrib import admin
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter

from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title',  'created_on','last_modified','description', 'status','id')
    list_display_links = ('id','title','author')
    list_filter = ('status', 'author', 'created_on','last_modified')
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "parent", "id")
    list_display_links = ('id','name')
    mptt_level_indent = 20
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "parent")
    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author','body','created_on','post','id')
    list_display_links = ('author','body','id')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "phone", "email_two")
    search_fields = ("user", "first_name", "last_name", "phone", "email_two")
    prepopulated_fields = {"slug": ("user",)}
