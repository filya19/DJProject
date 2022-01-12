from django.contrib import admin

from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_title', 'post_description', 'publish', 'status')
    list_filter = ('status', 'post_date', 'publish', 'author')
    search_fields = ('post_title', 'post_description')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
