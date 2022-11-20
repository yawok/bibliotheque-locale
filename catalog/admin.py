from django.contrib import admin
from .models import Book, BookInstance, Author, Language, Genre
from django_countries.widgets import CountrySelectWidget


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    
    
class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    fields = ('title', 'isbn', 'language')
    
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth','date_of_death')
    fields = ['first_name', 'last_name', 'nationality', ('date_of_birth', 'date_of_death'),]
    widgets = {'nationality': CountrySelectWidget()}
    inlines = [BookInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'is_overdue', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields' : ('book', 'imprint', 'id') 
        }),
        ('Availability', {
            'fields' : ('status', 'due_back', 'borrower',)
        }),
    )
    
    
admin.site.register(Language)
admin.site.register(Genre)