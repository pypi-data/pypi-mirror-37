# Short Text Field for Django

A very simple Django app that adds a `ShortTextField` model field class, which
is treated like a `TextField` in the database (i.e. the data is stored in the
database with the `text` rather than the `varchar` type, and the developer does
not need to specify a `max_length`), but uses the `TextInput` widget (a single-
line `<input type="text>`) by default rather than `Textarea`. This is ideal for
PostgreSQL, which recommends the 'text' type in a wider variety of
circumstances than other commonly-used database backends (see the
[PostgreSQL docs](https://www.postgresql.org/docs/9.1/static/datatype-character.html)).

## Installation

This package is available from
[PyPI](https://pypi.org/project/django-short-text-field/), so you can install
it using `pip` like this:

    pip install django-short-text-field

## Usage

1. Add `'short_text_field'` to your `INSTALLED_APPS` setting like this:

       INSTALLED_APPS = [
           ...
             'short_text_field',
       ]

2. Add a `ShortTextField` to a model like this:

       from short_text_field.models import ShortTextField
    
       ...

         class ExampleModel(models.Model):
               ...
               example_field = ShortTextField

3. A model with a `ShortTextField` should be registered in the admin site using
   `short_text_field.admin.ModelAdmin`.

       admin.site.register(ExampleModel, short_text_field.admin.ModelAdmin)

    A subclass of this class will also work:

       class ExampleModelAdmin(short_text_field.admin.ModelAdmin):
           model = ExampleModel
           ...

       admin.site.register(ExampleModel, ExampleModelAdmin)

   If you have a hierarchy of `ModelAdmin` subclasses, you can still
   incorporate `short_text_field.admin.ModelAdmin` easily as a mixin:

       class ExampleModelAdmin2(short_text_field.admin.ModelAdmin, ExampleModelAdmin1):
           model = ExampleModel
           ...

       admin.site.register(ExampleModel, ExampleModelAdmin)

   You can also use a subclass of `short_text_field.admin.AdminSite` for the
   site, which will make `short_text_field.admin.ModelAdmin` the default
   `ModelAdmin` subclass to use for registering. In the simplest case, you can
   just set the `default_site` attribute of the `AdminConfig` class and then
   register all of your models in the normal way:

       from django.contrib.admin import apps
       import short_text_field.admin.AdminSite

       ...

       class ExampleAdminConfig(apps.AdminConfig):
           ...
           default_site = short_text_field.admin.AdminSite