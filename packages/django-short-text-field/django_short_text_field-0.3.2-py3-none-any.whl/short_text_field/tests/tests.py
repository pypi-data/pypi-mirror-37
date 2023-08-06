from django.test import TestCase
from short_text_field.tests.models import TestModel

class ShortTextFieldTests(TestCase):
    def test_create(self):
        TestModel.objects.create()