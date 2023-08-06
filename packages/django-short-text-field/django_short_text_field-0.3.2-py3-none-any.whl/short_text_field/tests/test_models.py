from django.db import models
from django import forms
from django.test import TestCase
from short_text_field.tests.models import TestModel

class ShortTextFieldTests(TestCase):
    def setUp(self):
        model = TestModel.objects.create()
        self.field = model._meta.get_field('test_field')

    def test_field_is_db_text(self):
        self.assertIsInstance(self.field, models.TextField)

    def test_field_formfield_has_textinput(self):
        self.assertIsInstance(self.field.formfield().widget, forms.TextInput)