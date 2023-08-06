from django.contrib import admin
from django import forms
from short_text_field.models import ShortTextField

class ModelAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        # this part is copied from the django source
        if db_field.choices:
            return self.formfield_for_choice_field(db_field, request, **kwargs)

        if isinstance(db_field, ShortTextField):
            kwargs['widget'] = forms.TextInput

        return super().formfield_for_dbfield(db_field, request, **kwargs)

class AdminSite(admin.AdminSite):
    def register(self, model_or_iterable, admin_class=None, **options):
        admin_class = admin_class or ModelAdmin
        super().register(model_or_iterable, admin_class, **options)