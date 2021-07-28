from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datetime import datetime
from requests import get
from firstapp.helpful_links import default_front_cover
from firstapp.models import Book


# Create your views here.


class ShowAllBooks(View):

    def get(self, request):
        books = Book.objects.all()
        if request.GET:
            title = request.GET.get('ftitle')
            authors = request.GET.get('fauthor')
            language = request.GET.get('flg')
            date_start = request.GET.get('fdate-start')
            date_end = request.GET.get('fdate-end')
            if title:
                books = books.filter(title__iregex=r''+f'{title}')
            if authors:
                books = books.filter(authors__iregex=r''+f'{authors}')
            if language:
                books = books.filter(language__iregex=language)
            if date_start:
                date_start = datetime.strptime(date_start, '%Y-%m-%d')
                books = books.filter(published_date__gte=date_start)
            if date_end:
                date_end = datetime.strptime(date_end, '%Y-%m-%d')
                books = books.filter(published_date__lte=date_end)
            return render(request, 'firstapp/all_books.html', {'books': books})
        else:
            return render(request, 'firstapp/all_books.html', {'books': books})


class AddNewBook(CreateView):

    model = Book
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('all-books')


class EditBook(UpdateView):

    model = Book
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('all-books')


class DeleteBook(DeleteView):

    model = Book
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('all-books')


class ImportBookFromAPI(View):

    def get_url_api(self):
        url_API = 'https://www.googleapis.com/books/v1/volumes?q='
        if self.request.GET:
            for key in self.request.GET:
                value = self.request.GET.get(f'{key}')
                if value is not None and value != '':
                    url_API = url_API + f'+{key}:{value}'
        return url_API

    def get(self, request):

        response = get(self.get_url_api())
        if response.status_code == 200:
            r = response.json()
            for item in r['items']:
                volumeInfo = item['volumeInfo']

                try:
                    title = volumeInfo['title']
                except KeyError:
                    title = 'Untitled'

                try:
                    authors = ', '.join(volumeInfo['authors'])
                except KeyError:
                    authors = 'Unknown'

                try:
                    published_date = volumeInfo['publishedDate']
                    if len(published_date) == 4:
                        published_date += '-01-01'
                    if len(published_date) == 7:
                        published_date += '-01'
                except KeyError:
                    published_date = None

                try:
                    for number in volumeInfo['industryIdentifiers']:
                        if number['type'] == 'ISBN_10':
                            isbn_10 = number['identifier']
                        elif number['type'] == 'ISBN_13':
                            isbn_13 = number['identifier']
                except KeyError:
                    isbn_10 = None
                    isbn_13 = None

                try:
                    page_count = volumeInfo['pageCount']
                except KeyError:
                    page_count = None

                try:
                    front_cover_link = volumeInfo['imageLinks']['thumbnail']
                except KeyError:
                    front_cover_link = default_front_cover

                try:
                    language = volumeInfo['language']
                except KeyError:
                    language = 'Unknown'
                try:
                    Book.objects.update_or_create(
                        title=title,
                        authors=authors,
                        published_date=datetime.strptime(published_date, '%Y-%m-%d'),
                        ISBN_10=isbn_10,
                        ISBN_13=isbn_13,
                        page_count=page_count,
                        front_cover_link=front_cover_link,
                        language=language
                    )
                except IntegrityError:
                    warning = "Something went wrong :("
                    return render(request, 'firstapp/import_book_from_API.html', {'warning': warning})
            return redirect(reverse_lazy('all-books'))
        return render(request, 'firstapp/import_book_from_API.html')
