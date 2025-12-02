from django.test import TestCase
from catalog.models import Book, Author, BookInstance, Genre
from django.urls import reverse
import datetime
from catalog.forms import RenewBookModelForm
from django.contrib.auth.models import User, Permission

class RenewBookModelFormTest(TestCase):

    def test_due_back_field_label(self):
        form = RenewBookModelForm()
        self.assertTrue(form.fields['due_back'].label == 'renewal date')

    def test_due_back_in_past(self):
        date_in_past = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookModelForm(data={'due_back': date_in_past})
        self.assertFalse(form.is_valid())
        self.assertIn('Invalid date - renewal in past', form.errors['due_back'])

    def test_due_back_too_far(self):
        date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        form = RenewBookModelForm(data={'due_back': date_in_future})
        self.assertFalse(form.is_valid())
        self.assertIn('Invalid date - renewal more than 4 weeks ahead', form.errors['due_back'])

    def test_due_back_valid(self):
        valid_date = datetime.date.today() + datetime.timedelta(weeks=2)
        form = RenewBookModelForm(data={'due_back': valid_date})
        self.assertTrue(form.is_valid())

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from catalog.models import Book, Author, BookInstance
import datetime

class RenewBookViewTest(TestCase):

    def setUp(self):
        # Создаем пользователя и даем право библиотекаря
        self.user = User.objects.create_user(username='librarian', password='12345')
        permission = Permission.objects.get(codename='can_mark_returned')
        self.user.user_permissions.add(permission)
        self.user.save()

        # Создаем книгу и экземпляр книги
        author = Author.objects.create(first_name='John', last_name='Doe')
        book = Book.objects.create(title='Test Book', author=author)
        self.book_instance = BookInstance.objects.create(
            book=book, 
            imprint='Test Imprint', 
            due_back=datetime.date.today(), 
            borrower=self.user, 
            status='o'
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.book_instance.pk}))
        self.assertRedirects(response, '/accounts/login/?next=/book/%s/renew/' % self.book_instance.pk)

    def test_logged_in_with_permission(self):
        self.client.login(username='librarian', password='12345')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.book_instance.pk}))
        self.assertEqual(response.status_code, 200)
