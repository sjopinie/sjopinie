from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from sjopinie_app.views import home_page


class HomePageTest(TestCase):
    def test_room_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html_response(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>SubjectsToolkit</title>', html)
        self.assertTrue(html.endswith('</html>'))


#DEVMSG: A unit test that always fails, placed it here to show all of you how unit tests in Django work!
#class NonsenseTest(TestCase):
#
#    def test_nonsense_maths(self):
#           self.assertEqual(1+1,3)
