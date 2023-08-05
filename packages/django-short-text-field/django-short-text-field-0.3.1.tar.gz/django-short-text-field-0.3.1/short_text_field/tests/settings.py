SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    'short_text_field',
    'short_text_field.tests',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}