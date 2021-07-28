from rest_framework import serializers
from firstapp.models import Book


class BookSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Book
        fields = ['title',
                  'authors',
                  'published_date',
                  'ISBN_10',
                  'ISBN_13',
                  'page_count',
                  'front_cover_link',
                  'language']
