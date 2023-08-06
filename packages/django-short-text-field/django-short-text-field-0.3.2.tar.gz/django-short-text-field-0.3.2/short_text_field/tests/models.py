from django.db import models
from short_text_field.models import ShortTextField

class TestModel(models.Model):
    test_field = ShortTextField()