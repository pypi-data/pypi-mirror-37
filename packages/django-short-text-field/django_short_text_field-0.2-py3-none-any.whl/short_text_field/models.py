from django.db import models
from django import forms
from django.utils.translation import gettext as _

class ShortTextField(models.TextField):
	"""Like TextField in the database, like CharField in forms. No
	max_length argument required in initializer."""
	description = _('String')

	def formfield(self, **kwargs):
		defaults = {'form_class': forms.CharField}
		defaults.update(kwargs)
		return super().formfield(**defaults)