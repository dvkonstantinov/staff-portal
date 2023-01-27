from django.contrib import admin

from docs.models import Category, Document, Tag


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    list_display = ['id', 'title', 'description', 'author', 'category']
    list_display_links = ['id', 'title']


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id', 'title', 'slug']
    list_display_links = ['id', 'title']


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ['id', 'title', 'slug']
    list_display_links = ['id', 'title']


admin.site.register(Document, DocumentAdmin)
admin.site.register(Category, CategoryAdmin)
