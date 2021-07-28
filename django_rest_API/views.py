from firstapp.models import Book
from django_rest_API.serializers import BookSerializer
from django_rest_API.filters import BookFilter
from rest_framework import generics


class BookListAPI(generics.ListAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
