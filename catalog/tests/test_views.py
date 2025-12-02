from django.test import TestCase
from django.urls import reverse
from catalog.models import Author

class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_authors = 5
        for i in range(number_of_authors):
            Author.objects.create(first_name=f'Name{i}', last_name=f'Last{i}')

    def test_view_url_exists(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_template(self):
        response = self.client.get(reverse('authors'))
        self.assertTemplateUsed(response, 'catalog/author_list.html')
