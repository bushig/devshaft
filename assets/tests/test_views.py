from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve

from ..views import list, entry_details, add_entry


class AssetsURLConfTest(TestCase):

    def test_assets_list_url(self):
        found=resolve('/assets/')
        self.assertEqual(found.func, list)

    def test_assets_detail_url(self):
        found=resolve('/assets/167/')
        self.assertEqual(found.func, entry_details)

    def test_assets_add_url(self):
        found=resolve('/assets/add/')
        self.assertEqual(found.func, add_entry)