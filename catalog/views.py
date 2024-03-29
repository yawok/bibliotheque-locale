import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django_countries.widgets import CountrySelectWidget

from .models import Book, BookInstance, Author
from .forms import RenewBookModelForm


def index(request):
    """Returns the counts of books, book instances and authors."""
    number_of_books = Book.objects.all().count()
    number_of_book_instances = BookInstance.objects.all().count()
    number_of_available_book_instances = BookInstance.objects.filter(
        status__exact="a"
    ).count()
    number_of_authors = Author.objects.all().count()
    books_containing_of = Book.objects.filter(title__icontains="of").count()
    number_of_visits = request.session.get("number_of_visits", 0)
    request.session["number_of_visits"] = number_of_visits + 1

    context = {
        "number_of_books": number_of_books,
        "number_of_book_instances": number_of_book_instances,
        "number_of_available_book_instances": number_of_available_book_instances,
        "number_of_authors": number_of_authors,
        "books_containing_of": books_containing_of,
        "number_of_visits": number_of_visits,
    }

    return render(request, "catalog/index.html", context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """View to display books loaded to user"""

    model = BookInstance
    template_name = "catalog/books_borrowed_by_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class BorrowedListView(PermissionRequiredMixin, generic.ListView):
    permission_required = "catalog.can_mark_returned"
    model = BookInstance
    template_name = "catalog/all_borrowed_list.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")


@login_required
@permission_required("catalog.can_mark_returned", raise_exception=True)
def renew_book_labrarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":
        form = RenewBookModelForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data["due_back"]
            book_instance.save()

            return HttpResponseRedirect(reverse("borrowed"))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={"due_back": proposed_renewal_date})

    context = {"form": form, "book_instance": book_instance}

    return render(request, "catalog/book_renew_librarian.html", context)


class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "catalog.can_mark_returned"
    model = Author
    fields = [
        "first_name",
        "last_name",
        "nationality",
        "date_of_birth",
        "date_of_death",
    ]
    initial = {"date_of_birth": "2000-01-01"}
    widgets = {"nationality": CountrySelectWidget()}


class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "catalog.can_mark_returned"
    model = Author
    fields = "__all__"


class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "catalog.can_mark_returned"
    model = Author
    success_url = reverse_lazy("authors")


class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "catalog.can_add_book"
    model = Book
    fields = "__all__"


class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "catalog.can_add_book"
    model = Book
    fields = "__all__"


class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "catalog.can_add_book"
    model = Book
    success_url = reverse_lazy("books")
