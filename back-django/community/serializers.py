from rest_framework import serializers
from .models import Thread, Comment
from accounts.serializers import UserListSerializer
from books.serializers import BookSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('thread', 'user')

class ThreadListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Thread
        fields = ('id', 'user', 'book', 'book_title', 'title', 'rating', 'created_at', 'like_count', 'comment_count')
        read_only_fields = ('user', 'book')

class ThreadDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    
    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ('user', 'like_users')
