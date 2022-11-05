from django.shortcuts import render
from .models import Book, BookInstance, Author

def index(request):
    """Returns the counts of books, book instances and authors."""
    number_of_books = Book.objects.all().count()
    number_of_book_instances = BookInstance.objects.all().count()
    number_of_available_book_instances = BookInstance.objects.filter(status__exact='a').count()
    number_of_authors = Author.objects.all().count()
    books_containing_of = Book.objects.filter(title__icontains='of').count()
    
    context = {
        'number_of_books': number_of_books,
        'number_of_book_instances': number_of_book_instances,
        'number_of_available_book_instances': number_of_available_book_instances,
        'number_of_authors': number_of_authors,
        'books_containing_of': books_containing_of,
    }
    
    return render(request, 'index.html', context)