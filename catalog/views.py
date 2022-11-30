from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import generic

from catalog.models import Book, BookInstance, Author, Genre


def index(request):
    num_books = Book.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_books_available = Book.objects.filter(bookinstance__status__exact='A').count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {'num_books': num_books,
               'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors,
               'num_visits': num_visits,
               }
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'book_list'
    # queryset = Book.objects.filter(title__icontains='war')[:5]
    template_name = 'catalog/book_list.html'

    def get_queryset(self):
        return Book.objects.filter(title__icontains='life')[:5]

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(self, request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'

    def get_queryset(self):
        return Author.objects.filter(last_name__istartswith='s')[:5]


class AuthorDetailView(generic.DetailView):
    model = Author

    def book_detail_view(self, request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        return render(request, 'catalog/author_detail.html', context={'author': author})
