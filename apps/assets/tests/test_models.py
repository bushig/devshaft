from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Asset, Category

class EntryModelTests(TestCase):

    def setUp(self):
        category1 = Category.objects.create(category='Test category')
        user1 = User.objects.create(username = 'bushig', password = 'testpassword102', email = 'bushig@mail.ru')
        Asset.objects.get_or_create(category=category1, user=user1, name ='First asset', description ='Description for asset')

    def test_entry_could_be_deleted(self):
        entry = Asset.objects.get(name ='First asset')
        entry.delete()
        with self.assertRaises(Asset.DoesNotExist):
            Asset.objects.get(name ='First asset')

    def test_entry_can_add(self):
        entry = Asset.objects.create(category=Category.objects.first(), user=User.objects.first(), name ='Second asset', description ='Description for asset')
        self.assertEqual('Second asset', Asset.objects.get(name ='Second asset').name)