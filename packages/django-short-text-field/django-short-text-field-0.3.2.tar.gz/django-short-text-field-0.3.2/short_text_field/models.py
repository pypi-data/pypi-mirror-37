from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

class ShortTextField(models.TextField):
    """Like a TextField, but uses the TextInput rather than the TextArea widget
    in forms."""
    description = _('String')

    def formfield(self, **kwargs):
        defaults = {'widget': forms.TextInput}
        defaults.update(kwargs)
        return super().formfield(**defaults)