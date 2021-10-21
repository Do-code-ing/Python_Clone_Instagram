from django.contrib import admin
from instagram.models import *


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(HashTag)
admin.site.register(UserImage)
admin.site.register(PostTag)
