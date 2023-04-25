from django.shortcuts import render
# from django.http import HttpResponse
from .models import Book, Author, Bookinstance, Genre

def index(request):
    num_books = Book.objects.all().count()
    print(num_books)
    num_books1 = Book.objects.filter(title__exact='Steve Jobs').count()
    print(num_books1)
    num_instances = Bookinstance.objects.all().count()
    print(num_instances)
    num_instances_available = Bookinstance.objects.filter(book_status__exact='a').count()
    print(num_instances_available)
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_books1':num_books1,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)