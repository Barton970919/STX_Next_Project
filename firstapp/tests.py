from django.urls import reverse
import pytest
from firstapp.models import Book

# Create your tests here.


@pytest.mark.django_db
def test_all_books(client, new_book):
    assert Book.objects.count() == 1
    assert Book.objects.get(title='New book') == new_book
    response = client.get(reverse('all-books'), {'ftitle': "New book"})
    assert response.status_code == 200
    assert response.context['books'][0] == new_book


@pytest.mark.django_db
def test_add_new_book(client):
    response_get = client.get(reverse('add-new-book'))
    assert response_get.status_code == 200
    assert Book.objects.count() == 0
    response_post = client.post(reverse('add-new-book'), {'title': 'New book',
                                                          'authors': 'New Author',
                                                          'published_date': '2000-02-02',
                                                          'ISBN_10': '1234123',
                                                          'ISBN_13': '12312321',
                                                          'page_count': 123,
                                                          'front_cover_link': 'https://images-na.ssl-images-amazon.com/images/I/21u5Kw1n+IL._SX331_BO1,204,203,200_.jpg',
                                                          'language': 'pl'})
    assert response_post.status_code == 302
    assert Book.objects.count() == 1
    book = Book.objects.get(title='New book')
    assert book.authors == 'New Author'


@pytest.mark.django_db
def test_edit_book(client, new_book):
    assert Book.objects.count() == 1
    response_get = client.get(f'/edit_book/{new_book.id}/')
    assert response_get.status_code == 200
    response_post = client.post(f'/edit_book/{new_book.id}/', {'title': 'Edit book',
                                                               'authors': 'Edit Author',
                                                               'published_date': '2000-02-02',
                                                               'ISBN_10': '1234123',
                                                               'ISBN_13': '12312321',
                                                               'page_count': 123,
                                                               'front_cover_link': 'https://images-na.ssl-images-amazon.com/images/I/21u5Kw1n+IL._SX331_BO1,204,203,200_.jpg',
                                                               'language': 'pl'})
    assert response_post.status_code == 302
    book = Book.objects.get(pk=new_book.pk)
    assert book.title == "Edit book"


@pytest.mark.django_db
def test_delete_book(client, new_book):
    assert Book.objects.count() == 1
    response_get = client.get(f'/delete_book/{new_book.id}/')
    assert response_get.status_code == 200
    response_post = client.post(f'/delete_book/{new_book.id}/')
    assert response_post.status_code == 302
    assert Book.objects.count() == 0
