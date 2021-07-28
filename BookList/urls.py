"""BookList URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from firstapp.views import AddNewBook, ShowAllBooks, EditBook, DeleteBook, ImportBookFromAPI
from django_rest_API.views import BookListAPI


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ShowAllBooks.as_view(), name='all-books'),
    path('add_new_book/', AddNewBook.as_view(), name='add-new-book'),
    path('edit_book/<pk>/', EditBook.as_view(), name='edit-book'),
    path('delete_book/<pk>/', DeleteBook.as_view(), name='delete-book'),
    path('import_books/', ImportBookFromAPI.as_view(), name='import-books'),
    path('my_rest_api/', BookListAPI.as_view(), name='book-list-API')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
