from django.apps import AppConfig
from django.contrib.admin import apps

class ShortTextFieldConfig(apps.AppConfig):
    name = 'short_text_field'

class AdminConfig(apps.AdminConfig):
	default_site = 'short_text_field.admin.AdminSite'