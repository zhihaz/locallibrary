from django.test import TestCase
import datetime
from django.utils import timezone

from catalog.forms import RenewBookForm

class RenewBookFormTest(TestCase):

    def test_field_label(self):
        form = RenewBookForm()
        # Если label не указан, Django возвращает None, поэтому используем default
        self.assertEqual(form.fields['renewal_date'].label, None)  # Можно изменить на 'renewal date', если указали label в форме

    def test_help_text(self):
        form = RenewBookForm()
        self.assertEqual(
            form.fields['renewal_date'].help_text,
            "Enter a date between now and 4 weeks (default 3)."
        )

    def test_past_date_invalid(self):
        # Дата в прошлом должна вызвать ValidationError
        past_date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': past_date})
        self.assertFalse(form.is_valid())
        self.assertIn('renewal_date', form.errors)
        self.assertEqual(form.errors['renewal_date'][0], 'Invalid date - renewal in past')

    def test_future_date_too_far_invalid(self):
        # Дата больше чем 4 недели вперёд должна вызвать ValidationError
        future_date = datetime.date.today() + datetime.timedelta(weeks=5)
        form = RenewBookForm(data={'renewal_date': future_date})
        self.assertFalse(form.is_valid())
        self.assertIn('renewal_date', form.errors)
        self.assertEqual(form.errors['renewal_date'][0], 'Invalid date - renewal more than 4 weeks ahead')

    def test_valid_date(self):
        # Дата в пределах допустимого диапазона
        valid_date = datetime.date.today() + datetime.timedelta(weeks=2)
        form = RenewBookForm(data={'renewal_date': valid_date})
        self.assertTrue(form.is_valid())
