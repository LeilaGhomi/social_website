from django.contrib import admin

# from apps.post.models import Post, Comment, Like

from apps.post.models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'created_date']
    readonly_fields = ['created_date']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'note', 'created_date']
    readonly_fields = ['created_date']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'user_id', 'created_date']
    readonly_fields = ['created_date']
