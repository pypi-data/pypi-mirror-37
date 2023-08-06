from django.contrib import admin
from django import forms
from django.test import TestCase
import short_text_field.admin
from short_text_field.tests.models import TestModel

class MockRequest:
    pass

request = MockRequest()

class ModelAdminTests(TestCase):
    def setUp(self):
        site = admin.AdminSite()
        model_admin = short_text_field.admin.ModelAdmin(TestModel, admin_site=site)
        self.field = model_admin.get_form(request).base_fields['test_field']

    def test_formfield_has_textinput(self):
        self.assertIsInstance(self.field.widget, forms.TextInput)

class AdminSiteTests(TestCase):
    def setUp(self):
        site = short_text_field.admin.AdminSite()
        site.register(TestModel)
        model_admin = site._registry[TestModel]
        self.field = model_admin.get_form(request).base_fields['test_field']

    def test_formfield_has_textinput(self):
        self.assertIsInstance(self.field.widget, forms.TextInput)