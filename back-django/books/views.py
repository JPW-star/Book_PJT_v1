from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def book_detail(request, isbn13):
    book = get_object_or_404(Book, pk=isbn13)
    serializer = BookSerializer(book)
    return Response(serializer.data)
