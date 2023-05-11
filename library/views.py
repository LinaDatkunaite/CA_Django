from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Book, Author, Bookinstance, Genre
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages



def index(request):
    num_books = Book.objects.all().count()
    num_books1 = Book.objects.filter(title__exact='Steve Jobs').count()
    num_instances = Bookinstance.objects.all().count()
    num_instances_available = Bookinstance.objects.filter(book_status__exact='a').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_books': num_books,
        'num_books1':num_books1,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
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
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) |
                                         Q(author__first_name__icontains=query) )
    return render(request, 'search.html', {'books': search_results, 'query': query})





class UserBooksListView(LoginRequiredMixin, generic.ListView):
    model = Bookinstance
    template_name = 'user_books.html'
    paginate_by = 2

    def get_queryset(self):
        return Bookinstance.objects.filter(reader=self.request.user).filter(book_status__exact='t').order_by('due_back')


@login_required(login_url='login')
def user_books(request):
    user = request.user
    try:
        user_books = Bookinstance.objects.filter(reader=request.user).filter(book_status__exact='t').order_by('due_back')
    except Bookinstance.DoesNotExist:
        user_books = None
    context = {
        'user': user,
        'user_books': user_books,
    }
    return render(request, 'user_books1.html', context=context)

@csrf_protect
def register(request):
    if request.method == "POST":
        # taking from user form:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # checkai:
        # if passwords not match rise message
        if password != password2:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
        # if user already exists rise message
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Vartotojo vardas {username} užimtas!')
            return redirect('register')
        # if email already exists rise message
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
            return redirect('register')

        # if above checks pass, create new user
        User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        messages.info(request, f'Vartotojas {username} užregistruotas!')
        return redirect('login')

    return render(request, 'registration/register.html')
