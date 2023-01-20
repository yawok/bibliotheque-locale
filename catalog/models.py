from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import admin

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

import uuid
from datetime import date


class Genre(models.Model):
    """A model for Book Genre."""
    name = models.CharField(max_length=255, help_text="Enter a book genre.(Eg: Science Fiction)")
    
    
    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    """A model for Book"""
    title = models.CharField(max_length=255, help_text="Enter a book title")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField("ISBN", max_length=13, unique=True, help_text="13 Character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>")
    genre = models.ManyToManyField(Genre, help_text="Select a book genre")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    
    def __str__(self):
        return self.title
    
    
    def display_genre(self):
        """Create a list of the book's genre required for display in the Admin interface."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    
    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
    
    class Meta:
        ordering = ['title']
        permissions = (('can_add_book', 'Can add new book'),)
        
    
class BookInstance(models.Model):
    """A model for a book instance."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID of this book for the whole library.")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=255)
    due_back = models.DateField(null=True, blank=True, help_text="YYYY-MM-DD")
    LOAN_STATUS = (
        ('m', 'Maintainance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)
        
    
    @admin.display(
        boolean=True,
        ordering='due_back',
        description='Over Due?'
    )
    def is_overdue(self):
        """Check if book instance is overdue."""
        return bool(self.due_back and (date.today() > self.due_back))
    
    def __str__(self):
        return f"{self.id} ({self.book.title})"
    
    
    
class Author(models.Model):
    """A model for Auther."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nationality = CountryField(multiple=True, blank_label='(select country)', help_text="Hold down “Control”, or “Command” on a Mac, to select more than one." )
    date_of_birth = models.DateField(null=True, blank=True, help_text="YYYY-MM-DD")
    date_of_death = models.DateField('died', null=True, blank=True, help_text="YYYY-MM-DD")
    
    
    
    class Meta:
        ordering = ['last_name', 'first_name']
        
    
    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])
    

    def get_full_name(self):
        """Return author's full name"""
        return f'{self.last_name}, {self.first_name}'
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    
    
class Language(models.Model):
    """A model for languages."""
    name = models.CharField(max_length=255, help_text="Enter the book's natural language(Eg: English, French")
    
    
    def __str__(self):
        return self.name
    
