from django.contrib import admin
from .models import Thread, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'book', 'rating', 'created_at')
    list_filter = ('created_at', 'rating')
    search_fields = ('title', 'content', 'user__username', 'book__title')
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'thread', 'created_at')
    search_fields = ('content', 'user__username')
