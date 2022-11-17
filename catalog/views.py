from django.shortcuts import render
from django.views import generic
from .models import Book, BookInstance, Author
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """Returns the counts of books, book instances and authors."""
    number_of_books = Book.objects.all().count()
    number_of_book_instances = BookInstance.objects.all().count()
    number_of_available_book_instances = BookInstance.objects.filter(status__exact='a').count()
    number_of_authors = Author.objects.all().count()
    books_containing_of = Book.objects.filter(title__icontains='of').count()
    number_of_visits = request.session.get('number_of_visits', 0)
    request.session['number_of_visits'] = number_of_visits + 1 
    
    context = {
        'number_of_books': number_of_books,
        'number_of_book_instances': number_of_book_instances,
        'number_of_available_book_instances': number_of_available_book_instances,
        'number_of_authors': number_of_authors,
        'books_containing_of': books_containing_of,
        'number_of_visits': number_of_visits,
    }
    
    return render(request, 'catalog/index.html', context)


class BookListView(generic.ListView):
    model = Book
    
    
class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10
    
    
class AuthorListView(generic.ListView):
    model = Author
    
    
class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 10

    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """View to display books loaded to user"""
    model = BookInstance
    template_name = 'catalog/books_borrowed_by_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    