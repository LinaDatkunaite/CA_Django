from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Book, Author, Bookinstance, Genre
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    num_books = Book.objects.all().count()
    num_books1 = Book.objects.filter(title__exact='Steve Jobs').count()
    num_instances = Bookinstance.objects.all().count()
    num_instances_available = Bookinstance.objects.filter(book_status__exact='a').count()
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


def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors
    }
    return render(request, 'authors.html', context=context)

def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author': single_author})





# class based approach to create views

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3
    template_name = 'book_list.html'

class RomeoBookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    queryset = Book.objects.filter(title__icontains='Romeo')[:3]
    template_name = 'romeo_list.html'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'




def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(author__first_name__icontains=query) )
    return render(request, 'search.html', {'books': search_results, 'query': query})