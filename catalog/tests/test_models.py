from django.test import TestCase

from catalog.models import Author, Book, Genre, Language, BookInstance

import datetime


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create non-modified objects used by all text methods"""
        Author.objects.create(first_name="Kenneth", last_name="Obeng")

    def test_first_name_label(self):
        author = Author.objects.get(pk=1)
        field_label = author._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_last_name_label(self):
        author = Author.objects.get(pk=1)
        field_label = author._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")

    def test_nationality_label(self):
        author = Author.objects.get(pk=1)
        field_label = author._meta.get_field("nationality").verbose_name
        self.assertEqual(field_label, "nationality")

    def test_date_of_birth_label(self):
        author = Author.objects.get(pk=1)
        field_label = author._meta.get_field("date_of_birth").verbose_name
        self.assertEqual(field_label, "date of birth")

    def test_date_of_death_label(self):
        author = Author.objects.get(pk=1)
        field_label = author._meta.get_field("date_of_death").verbose_name
        self.assertEqual(field_label, "died")

    def test_first_name_max_lenght(self):
        author = Author.objects.get(pk=1)
        max_length = author._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(pk=1)
        expected_name = f"{author.last_name}, {author.first_name}"
        self.assertEqual(str(author), expected_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(pk=1)
        self.assertEqual(author.get_absolute_url(), "/catalog/authors/1")


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(first_name="Kenneth", last_name="Obeng")
        genre1 = Genre.objects.create(name="Fiction")
        genre2 = Genre.objects.create(name="Adventure")
        language = Language.objects.create(name="English")
        book = Book.objects.create(
            title="Cell",
            author=author,
            summary="See ee el el, Cell",
            isbn="123sdf123asd7",
            language=language,
        )
        book.genre.add(genre1, genre2)

    def test_title_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")

    def test_author_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("author").verbose_name
        self.assertEqual(field_label, "author")

    def test_isbn_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("isbn").verbose_name
        self.assertEqual(field_label, "ISBN")

    def test_summary_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("summary").verbose_name
        self.assertEqual(field_label, "summary")

    def test_genre_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("genre").verbose_name
        self.assertEqual(field_label, "genre")

    def test_language_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("language").verbose_name
        self.assertEqual(field_label, "language")

    def test_title_max_length(self):
        book = Book.objects.get(pk=1)
        max_length = book._meta.get_field("title").max_length
        self.assertEqual(max_length, 255)

    def test_summary_max_length(self):
        book = Book.objects.get(pk=1)
        max_length = book._meta.get_field("summary").max_length
        self.assertEqual(max_length, 1000)

    def test_isbn_max_length(self):
        book = Book.objects.get(pk=1)
        max_length = book._meta.get_field("isbn").max_length
        self.assertEqual(max_length, 13)

    def test_display_genre(self):
        book = Book.objects.get(pk=1)
        self.assertEqual(book.display_genre(), "Fiction, Adventure")

    def test_get_absolute_url(self):
        book = Book.objects.get(pk=1)
        self.assertEqual(book.get_absolute_url(), "/catalog/books/1")

    def test_object_name_is_title_of_book(self):
        book = Book.objects.get(pk=1)
        self.assertEqual(str(book), book.title)


class BookInstanceModelTest(TestCase):

    id1 = 0
    id2, id3 = 0, 0

    @classmethod
    def setUpTestData(cls):
        global id1, id2, id3
        author = Author.objects.create(first_name="Kenneth", last_name="Obeng")
        genre1 = Genre.objects.create(name="Fiction")
        genre2 = Genre.objects.create(name="Adventure")
        language = Language.objects.create(name="English")
        book = Book.objects.create(
            title="Cell",
            author=author,
            summary="See ee el el, Cell",
            isbn="123sdf123asd7",
            language=language,
        )
        book.genre.add(genre1, genre2)
        id1 = BookInstance.objects.create(book=book, imprint="Disney", status="a").id
        id2 = BookInstance.objects.create(
            book=book,
            imprint="Disney",
            status="o",
            due_back=(datetime.date.today() - datetime.timedelta(weeks=3)),
        ).id
        id3 = BookInstance.objects.create(
            book=book,
            imprint="Disney",
            status="o",
            due_back=(datetime.date.today() - datetime.timedelta(days=4)),
        ).id

    def test_book_label(self):
        book = BookInstance.objects.get(pk=id1)
        field_label = book._meta.get_field("book").verbose_name
        self.assertEqual(field_label, "book")

    def test_imprint_label(self):
        book = BookInstance.objects.get(pk=id1)
        field_label = book._meta.get_field("imprint").verbose_name
        self.assertEqual(field_label, "imprint")

    def test_status_label(self):
        book = BookInstance.objects.get(pk=id1)
        field_label = book._meta.get_field("status").verbose_name
        self.assertEqual(field_label, "status")

    def test_id_label(self):
        book = BookInstance.objects.get(pk=id1)
        field_label = book._meta.get_field("id").verbose_name
        self.assertEqual(field_label, "id")

    def test_due_back_label(self):
        book = BookInstance.objects.get(pk=id1)
        field_label = book._meta.get_field("due_back").verbose_name
        self.assertEqual(field_label, "due back")

    def test_borrower_label(self):
        book = BookInstance.objects.get(pk=id1)
        field_label = book._meta.get_field("borrower").verbose_name
        self.assertEqual(field_label, "borrower")

    def test_is_overdue(self):
        book = BookInstance.objects.get(pk=id2)
        self.assertTrue(book.is_overdue)

    def test_object_name_is_id_title_in_brackets(self):
        book = BookInstance.objects.get(pk=id2)
        expected_name = f"{id2} (Cell)"
        self.assertEqual(str(book), expected_name)

    def test_object_name_is_id_title_in_brackets(self):
        book1 = BookInstance.objects.get(pk=id1)
        book2 = BookInstance.objects.get(pk=id2)
        book3 = BookInstance.objects.get(pk=id3)
        query = list(BookInstance.objects.all())
        expected_order = [book1, book2, book3]
        self.assertEqual(query, expected_order)


class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create non-modified objects used by all text methods"""
        Genre.objects.create(name="Fiction")

    def test_name_label(self):
        genre = Genre.objects.get(pk=1)
        field_label = genre._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_object_name_is_id_title_in_brackets(self):
        genre = Genre.objects.get(pk=1)
        self.assertEqual(str(genre), "Fiction")


class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create non-modified objects used by all text methods"""
        Language.objects.create(name="French")

    def test_name_label(self):
        language = Language.objects.get(pk=1)
        field_label = language._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_object_name_is_id_title_in_brackets(self):
        language = Language.objects.get(pk=1)
        self.assertEqual(str(language), "French")
