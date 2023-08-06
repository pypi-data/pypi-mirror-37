from django.contrib import admin

from blogs.models import Post, Author

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('uuid', 'heading', 'is_published')
    list_filter = ('is_published', 'is_deleted')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ('user', 'is_author')
    list_filter = ('is_author', )