from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Entry, Category

class EntryModelTests(TestCase):

    def setUp(self):
        category1 = Category.objects.create(category='Test category')
        user1 = User.objects.create(username = 'bushig', password = 'testpassword102', email = 'bushig@mail.ru')
        Entry.objects.get_or_create(category=category1, user=user1, name = 'First asset', description = 'Description for asset')

    def test_entry_could_be_deleted(self):
        entry = Entry.objects.get(name = 'First asset')
        entry.delete()
        with self.assertRaises(Entry.DoesNotExist):
            Entry.objects.get(name = 'First asset')

    def test_entry_can_add(self):
        entry = Entry.objects.create(category=Category.objects.first(), user=User.objects.first(), name = 'Second asset', description = 'Description for asset')
        self.assertEqual('Second asset', Entry.objects.get(name = 'Second asset').name)