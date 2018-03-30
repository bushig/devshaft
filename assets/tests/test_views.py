from django.test import TestCase, LiveServerTestCase, Client
from django.contrib.auth.models import User
from django.urls import resolve, reverse

from ..views import assets_list, entry_details, add_entry


class AssetsURLConfTest(TestCase):

    def test_assets_list_url(self):
        found=resolve(reverse('assets:list'))
        self.assertEqual(found.func, assets_list)

    def test_assets_detail_url(self):
        found=resolve(reverse('assets:detail'))
        self.assertEqual(found.func, entry_details)

    def test_assets_add_url(self):
        found=resolve(reverse('assets:add_entry'))
        self.assertEqual(found.func, add_entry)


class AssetsListViewTest(TestCase):

    def setUp(self):
        user=User(username='testuser', email='test@mail.com')
        user.set_password('qwerty1')
        user.save()

    def test_anon_user_cant_get_add_assets_page(self):
        c=Client()
        response=c.get(reverse('assets:add_entry'))
        self.assertEqual(response.url, '/accounts/login/?next=/add/', 'Should redirect to login page')
        self.assertEqual(response.status_code, 302)

    def test_user_can_get_add_assets_page(self):
        c=Client()
        c.login(username='testuser', password='qwerty1')
        response=c.get(reverse('assets:add_entry'))
        self.assertEqual(response.status_code, 200, 'Should open page')