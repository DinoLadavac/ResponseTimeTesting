from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.views.generic import ListView
from .forms import BookFilterForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import BookForm


## Create your views here.

class BookList(ListView):
    model = Book
    
    emplate_name = 'main/book_list.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Handle form submission
        form = BookFilterForm(self.request.GET)
        if form.is_valid():
            author = form.cleaned_data.get('author')
            publisher = form.cleaned_data.get('publisher')

            if author:
                queryset = queryset.filter(author=author)
            if publisher:
                queryset = queryset.filter(publisher=publisher)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookFilterForm(self.request.GET)
        return context

    
class AuthorList(ListView):
    model = Author


class PublisherList(ListView):
    model = Publisher

class PublisherBookList(ListView):
    template_name = 'main/book_list.html'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Book.objects.filter(publisher=self.publisher)

class AuthorBookList(ListView):
    template_name = 'main/book_list.html'

    def get_queryset(self):
        self.author = get_object_or_404(Author, name=self.kwargs['author'])
        return Book.objects.filter(author=self.author)
  
@csrf_exempt   
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../books')  # Redirect to the book list page
    else:
        form = BookForm()

    return render(request, 'main/add_book.html', {'form': form})

