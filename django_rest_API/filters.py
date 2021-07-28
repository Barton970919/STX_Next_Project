import django_filters
from firstapp.models import Book


class BookFilter(django_filters.FilterSet):

    class Meta:
        model = Book
        fields = {
            'title': ['iregex'],
            'authors': ['iregex'],
            'language': ['iregex'],
            'published_date': ['gte', 'lte']
        }
