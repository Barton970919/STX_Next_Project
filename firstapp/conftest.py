from datetime import datetime

import pytest
from django.test import Client
from firstapp.models import Book

@pytest.fixture()
def client():
    client = Client()
    return client

@pytest.fixture()
def new_book():
    new_book = Book.objects.create(
        title='New book',
        authors='New Author',
        published_date=datetime.strptime('2000-02-02', "%Y-%m-%d"),
        page_count=123,
        front_cover_link='https://images-na.ssl-images-amazon.com/images/I/21u5Kw1n+IL._SX331_BO1,204,203,200_.jpg',
        language='pl'
    )
    return new_book

