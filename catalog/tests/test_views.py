import datetime
import uuid

from django.utils import timezone 
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission

from catalog.models import Author, Book, BookInstance, Genre, Language


class IndexViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('')
        #redirect to a Moved Permanently url(code 301)
        self.assertEqual(response.status_code, 301)
        
        
    def test_view_url_is_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
        
    def test_view_uses_correct_template(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/index.html')
        
    
    def test_view_session_counts_number_of_visits(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['number_of_visits'], 0)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['number_of_visits'], 1)
        response = self.client.get(reverse('index'))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['number_of_visits'], 3)



class BookListViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        no_of_books = 15
        test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
        )
        genre = Genre.objects.create(name='Adventure')
        test_language = Language.objects.create(name='English')
       
        for book in range(no_of_books):
            test_book = Book.objects.create(
                title=f"Cell{book}",
                summary="See ee el el, Cell", isbn=f'123sdf123asd{book}',
                author=test_author, 
                language=test_language)
            genre_objects_for_book = Genre.objects.all()
            test_book.genre.set(genre_objects_for_book)
            test_book.save()
        
        
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/books/')
        self.assertEqual(response.status_code, 200)
        
        
    def test_view_url_is_accessible_by_name(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        
        
    def test_view_uses_correct_template(self):
        response = self.client.get('/catalog/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_list.html')
        
    
    def test_pagination_is_10(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['book_list']), 10)


    def test_pagination_of_the_rest_of_book_list(self):
        response = self.client.get(reverse('books') +'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['book_list']), 5)


class BookDetailViewTest(TestCase):
    
    def setUp(self):
        
        test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
            )
        test_genre = Genre.objects.create(name='Adventure')
        test_language = Language.objects.create(name='English')
        self.test_book = Book.objects.create(
            title="Cell",
            summary="See ee el el, Cell", isbn='123sdf123asd7',
            author=test_author, 
            language=test_language)
        genre_objects_for_book = Genre.objects.all()
        self.test_book.genre.set(genre_objects_for_book)
        self.test_book.save()
        
        no_of_book_copies = range(30)
        
        for book_copy in no_of_book_copies:
            return_date = datetime.date.today() + timezone.timedelta(days=book_copy%5)
            status = 'm'
            BookInstance.objects.create(
                book=self.test_book, 
                imprint='Disney', 
                status=status,
            )

    
    def test_view_url_is_accessible_by_name(self):
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.test_book.id }))
        self.assertEqual(response.status_code, 200)

        
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/catalog/books/{self.test_book.id}')
        self.assertEqual(response.status_code, 200)
        
    def test_logged_in_uses_correct_template(self):
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.test_book.id }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_detail.html')
        
                  

class AuthorListViewTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
       no_of_authors = 15
       
       for author in range(no_of_authors):
           Author.objects.create(first_name=f'Author{author}', last_name=f'Green{author}')
        
        
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)
        
        
    def test_view_url_is_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        
        
    def test_view_uses_correct_template(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')
        
    
    def test_pagination_is_10(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)


    def test_pagination_of_the_rest_of_author_list(self):
        response = self.client.get(reverse('authors') +'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 5)


class AuthorDetailViewTest(TestCase):
    
    def setUp(self):
        
        self.test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
            )

    
    def test_view_url_is_accessible_by_name(self):
        response = self.client.get(reverse('author-detail', kwargs={'pk': self.test_author.id }))
        self.assertEqual(response.status_code, 200)

        
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/catalog/authors/{self.test_author.id}')
        self.assertEqual(response.status_code, 200)
        
    def test_logged_in_uses_correct_template(self):
        response = self.client.get(reverse('author-detail', kwargs={'pk': self.test_author.id }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_detail.html')
        
                  
class LoanedBookInstanceByUserListViewTest(TestCase):
    
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='adamu1234')
        test_user2 = User.objects.create_user(username='testuser2', password='adamu1234')

        test_user1.save()
        test_user2.save()
        
        test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
            )
        test_genre = Genre.objects.create(name='Adventure')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title="Cell",
            summary="See ee el el, Cell", isbn='123sdf123asd7',
            author=test_author, 
            language=test_language)
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()
        
        no_of_book_copies = range(30)
        
        for book_copy in no_of_book_copies:
            return_date = datetime.date.today() + timezone.timedelta(days=book_copy%5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'm'
            BookInstance.objects.create(
                book=test_book, 
                imprint='Disney', 
                status=status,
                due_back=return_date,
                borrower=the_borrower 
                )

    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')

        
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='adamu1234')
        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/books_borrowed_by_user.html')
        

    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='testuser1', password='adamu1234')
        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/books_borrowed_by_user.html')
        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 0)
        
        books = BookInstance.objects.all()[:10]    
        for book in books:
            book.status = 'o'
            book.save()
            
        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 5)

        for book_item in response.context['bookinstance_list']:
            self.assertEqual(response.context['user'], book_item.borrower)
            self.assertEqual(book_item.status, 'o')

 
    def test_pages_ordered_by_due_date(self):
        login = self.client.login(username='testuser1', password='adamu1234')
        books = BookInstance.objects.all()    
        for book in books:
            book.status = 'o'
            book.save()
            
        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['bookinstance_list']), 10)

        last_date = 0
        for book in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back


class BorrowedListViewTest(TestCase):
    
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='adamu1234')
        test_user2 = User.objects.create_user(username='testuser2', password='adamu1234')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
            )
        test_genre = Genre.objects.create(name='Adventure')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title="Cell",
            summary="See ee el el, Cell", isbn='123sdf123asd7',
            author=test_author, 
            language=test_language)
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()
        
        no_of_book_copies = range(30)
        
        for book_copy in no_of_book_copies:
            return_date = datetime.date.today() + timezone.timedelta(days=book_copy%5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'm'
            BookInstance.objects.create(
                book=test_book, 
                imprint='Disney', 
                status=status,
                due_back=return_date,
                borrower=the_borrower 
                )

    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('borrowed'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/borrowed/')

        
    def test_logged_in_without_correct_permissions(self):
        login = self.client.login(username='testuser1', password='adamu1234')
        response = self.client.get(reverse('borrowed'))
        self.assertEqual(response.status_code, 403)
        

    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/all_borrowed_list.html')
        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 0)
        
        books = BookInstance.objects.all()[:10]    
        for book in books:
            book.status = 'o'
            book.save()
            
        response = self.client.get(reverse('borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 10)

        for book_item in response.context['bookinstance_list']:
            self.assertEqual(book_item.status, 'o')

 
    def test_pages_ordered_by_due_date(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        books = BookInstance.objects.all()    
        for book in books:
            book.status = 'o'
            book.save()
            
        response = self.client.get(reverse('borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['bookinstance_list']), 10)

        last_date = 0
        for book in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back




           
class RenewBookInstancesViewTest(TestCase):
    
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='adamu1234')
        test_user2 = User.objects.create_user(username='testuser2', password='adamu1234')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
            )
        test_genre = Genre.objects.create(name='Adventure')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title="Cell",
            summary="See ee el el, Cell", isbn='123sdf123asd7',
            author=test_author, 
            language=test_language)
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()
        
    
        return_date = datetime.date.today() + timezone.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book, 
            imprint='Disney', 
            status='o',
            due_back=return_date,
            borrower=test_user1 
            )
        
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book, 
            imprint='Disney', 
            status='o',
            due_back=return_date,
            borrower=test_user2 
            )
     
     
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('renew-book-librarian' ,kwargs={'pk': self.test_bookinstance1.pk }))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith, '/accounts/login/')
        
        
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='adamu1234')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk }))
        self.assertEqual(response.status_code, 403)
        
        
    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk }))
        self.assertEqual(response.status_code, 200)
        
    
    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk }))
        self.assertEqual(response.status_code, 200)
        
        
    def test_HTTP404_for_invalid_book_if_logged_in(self):
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': test_uid }))
        self.assertEqual(response.status_code, 404)
        
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_renew_librarian.html')
        
    
    def test_form_renewal_date_initailly_3_weeks_in_future(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk }))
        self.assertEqual(response.status_code, 200)   
        date_3_weeks_in_future = datetime.date.today() + timezone.timedelta(weeks=3)
        self.assertEqual(response.context['form'].initial['due_back'], date_3_weeks_in_future) 
        
    
    def test_redirect_to_all_borrowed_books_on_success(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        date_2_weeks_in_future = datetime.date.today() + timezone.timedelta(weeks=2)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk }), {'due_back': date_2_weeks_in_future})
        self.assertRedirects(response, reverse('borrowed'))
    
        
    def test_invalid_renewal_date_past(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        date_3_weeks_in_past = datetime.date.today() + timezone.timedelta(weeks=-3)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk }), {'due_back': date_3_weeks_in_past})
        self.assertTrue(response, 200)
        self.assertFormError(response, 'form', 'due_back', 'Invalid date - renewal date in the past')
     
    
    def test_invalid_renewal_date_future(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        date_7_weeks_in_future = datetime.date.today() + timezone.timedelta(weeks=7)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk }), {'due_back': date_7_weeks_in_future})
        self.assertTrue(response, 200)
        self.assertFormError(response, 'form', 'due_back', ['Invalid date - renewal date more than 4 weeks away.'])
     

     
class AuthorCreateViewTest(TestCase):
    
    def setUp(self):
        
        self.test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
            )
        
        test_user1 = User.objects.create_user(username='testuser1', password='adamu1234')
        test_user2 = User.objects.create_user(username='testuser2', password='adamu1234')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith, '/accounts/login/')
        
        
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='adamu1234')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 403)

    
    def test_view_url_is_accessible_by_name(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)

        
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get('/catalog/author/create')
        self.assertEqual(response.status_code, 301)
        
        
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_form.html')
        

class AuthorUpdateViewTest(TestCase):
    
    def setUp(self):
        
        self.test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
            )
        
        test_user1 = User.objects.create_user(username='testuser1', password='adamu1234')
        test_user2 = User.objects.create_user(username='testuser2', password='adamu1234')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()
    


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author-update', kwargs={'pk': self.test_author.id }))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith, '/accounts/login/')
        
        
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='adamu1234')
        response = self.client.get(reverse('author-update', kwargs={'pk': self.test_author.id}))
        self.assertEqual(response.status_code, 403)

    
    def test_view_url_is_accessible_by_name(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('author-update', kwargs={'pk': self.test_author.id}))
        self.assertEqual(response.status_code, 200)

        
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(f'/catalog/author/{self.test_author.id}/update')
        self.assertEqual(response.status_code, 301)
        
        
    def test_form_contains_correct_author_details(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('author-update', kwargs={'pk': self.test_author.id }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['first_name'], self.test_author.first_name)
        
        
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('author-update', kwargs={'pk': self.test_author.id }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_form.html')


class AuthorDeleteViewTest(TestCase):
    
    def setUp(self):
        
        self.test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
            )
        
        test_user1 = User.objects.create_user(username='testuser1', password='adamu1234')
        test_user2 = User.objects.create_user(username='testuser2', password='adamu1234')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()
    


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author-delete', kwargs={'pk': self.test_author.id }))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith, '/accounts/login/')
        
        
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='adamu1234')
        response = self.client.get(reverse('author-delete', kwargs={'pk': self.test_author.id}))
        self.assertEqual(response.status_code, 403)

    
    def test_view_url_is_accessible_by_name(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('author-delete', kwargs={'pk': self.test_author.id}))
        self.assertEqual(response.status_code, 200)

        
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(f'/catalog/author/{self.test_author.id}/delete')
        self.assertEqual(response.status_code, 301)
        
        
        
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('author-delete', kwargs={'pk': self.test_author.id }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_confirm_delete.html')

#########################  
class BookCreateViewTest(TestCase):
    
    def setUp(self):
        
        test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
            )
        
        test_user1 = User.objects.create_user(username='testuser1', password='adamu1234')
        test_user2 = User.objects.create_user(username='testuser2', password='adamu1234')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can add new book')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith, '/accounts/login/')
        
        
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='adamu1234')
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 403)

    
    def test_view_url_is_accessible_by_name(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 200)

        
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get('/catalog/book/create')
        self.assertEqual(response.status_code, 301)
        
        
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_form.html')
        

class BookUpdateViewTest(TestCase):
    
    def setUp(self):
        test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
            )
        
        test_user1 = User.objects.create_user(username='testuser1', password='adamu1234')
        test_user2 = User.objects.create_user(username='testuser2', password='adamu1234')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can add new book')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        test_genre = Genre.objects.create(name='Adventure')
        test_language = Language.objects.create(name='English')
        self.test_book = Book.objects.create(
            title="Cell",
            summary="See ee el el, Cell", isbn='123sdf123asd7',
            author=test_author, 
            language=test_language)
        genre_objects_for_book = Genre.objects.all()
        self.test_book.genre.set(genre_objects_for_book)
        self.test_book.save()


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author-update', kwargs={'pk': self.test_book.id }))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith, '/accounts/login/')
        
        
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='adamu1234')
        response = self.client.get(reverse('book-update', kwargs={'pk': self.test_book.id}))
        self.assertEqual(response.status_code, 403)

    
    def test_view_url_is_accessible_by_name(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('book-update', kwargs={'pk': self.test_book.id}))
        self.assertEqual(response.status_code, 200)

        
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(f'/catalog/book/{self.test_book.id}/update')
        self.assertEqual(response.status_code, 301)
        
        
    def test_form_contains_correct_author_details(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('book-update', kwargs={'pk': self.test_book.id }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['title'], self.test_book.title)
        
        
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('book-update', kwargs={'pk': self.test_book.id }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_form.html')


class BookDeleteViewTest(TestCase):
    
    def setUp(self):
        
        test_author = Author.objects.create(
            first_name='Kenneth', 
            last_name='Obeng'
            )
        
        test_user1 = User.objects.create_user(username='testuser1', password='adamu1234')
        test_user2 = User.objects.create_user(username='testuser2', password='adamu1234')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can add new book')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        test_genre = Genre.objects.create(name='Adventure')
        test_language = Language.objects.create(name='English')
        self.test_book = Book.objects.create(
            title="Cell",
            summary="See ee el el, Cell", isbn='123sdf123asd7',
            author=test_author, 
            language=test_language)
        genre_objects_for_book = Genre.objects.all()
        self.test_book.genre.set(genre_objects_for_book)
        self.test_book.save()
    


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('book-delete', kwargs={'pk': self.test_book.id }))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith, '/accounts/login/')
        
        
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='adamu1234')
        response = self.client.get(reverse('book-delete', kwargs={'pk': self.test_book.id}))
        self.assertEqual(response.status_code, 403)

    
    def test_view_url_is_accessible_by_name(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('book-delete', kwargs={'pk': self.test_book.id}))
        self.assertEqual(response.status_code, 200)

        
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(f'/catalog/book/{self.test_book.id}/delete')
        self.assertEqual(response.status_code, 301)
        
        
        
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='adamu1234')
        response = self.client.get(reverse('book-delete', kwargs={'pk': self.test_book.id }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_confirm_delete.html')
