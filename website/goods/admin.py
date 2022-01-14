from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'description', 'publish', 'status')
    list_filter = ('status', 'date', 'publish', 'author')
    search_fields = ('title', 'description')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)
