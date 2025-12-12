from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Thread, Comment
from books.models import Book
from .serializers import ThreadListSerializer, ThreadDetailSerializer, CommentSerializer

@api_view(['GET', 'POST'])
@permission_classes([AllowAny]) # GET is AllowAny, POST is IsAuthenticated handled inside
def thread_list_create(request):
    if request.method == 'GET':
        threads = Thread.objects.all().order_by('-created_at')
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # book_isbn13 comes from request data, need to fetch Book object
        # Assuming frontend sends 'book_isbn13'
        book_isbn = request.data.get('book_isbn13')
        book = get_object_or_404(Book, pk=book_isbn)
        
        serializer = ThreadListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny]) # GET AllowAny, others IsAuthenticated owner
def thread_detail(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)

    if request.method == 'GET':
        serializer = ThreadDetailSerializer(thread)
        return Response(serializer.data)
    
    # Permission Check for PUT/DELETE
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if thread.user != request.user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = ThreadDetailSerializer(thread, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, thread=thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user != request.user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def thread_likes(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)
    if thread.like_users.filter(pk=request.user.pk).exists():
        thread.like_users.remove(request.user)
        liked = False
    else:
        thread.like_users.add(request.user)
        liked = True
    return Response({'liked': liked, 'count': thread.like_users.count()})
