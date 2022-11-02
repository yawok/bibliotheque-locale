from django.db import models
from django.urls import reverse
import uuid


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
    
    
    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
    
    
    
class BookInstance(models.Model):
    """A model for a book instance."""
    uniqueid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID of this book for the whole library.")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=255)
    due_date = models.DateTimeField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintainance'),
        ('o', 'On load'),
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
    
    
    class Meta:
        ordering = ['due_date']
        
    
    def __str__(self):
        return f"{self.id} ({self.book.title})"
    
    
    
class Author(models.Model):
    """A model for Auther."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    date_of_death = models.DateTimeField('Died', null=True, blank=True)
    
    
    class Meta:
        ordering = ['last_name', 'first_name']
        
    
    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])
    

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    
    
class Language(models.Model):
    """A model for languages."""
    name = models.CharField(max_length=255, help_text="Enter the book's natural language(Eg: English, French")
    
    
    def __str__(self):
        return self.name
    