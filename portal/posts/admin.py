from django.contrib import admin

from posts.models import Post, PostCategory


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['id', 'title', 'author', 'created_at']
    list_display_links = ['id', 'title']


class PostCategoryAdmin(admin.ModelAdmin):
    model = PostCategory
    list_display = ['id', 'title', 'slug']
    list_display_links = ['id', 'title']


admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
