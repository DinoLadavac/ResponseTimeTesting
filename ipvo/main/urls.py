from django.urls import path
from . import views
from.views import *

app_name = 'main'

urlpatterns = [   
    path('publishers', PublisherList.as_view()),
    path('authors/', AuthorList.as_view()),
    path('pub/<publisher>', PublisherBookList.as_view()),
    path('author/<author>', AuthorBookList.as_view()),
    path('books/', BookList.as_view(), name="book_list"),
    path('add_book/', add_book, name='add_book'),
]