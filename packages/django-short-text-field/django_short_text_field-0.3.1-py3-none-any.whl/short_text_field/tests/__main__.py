import os
from pathlib import Path
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'short_text_field.tests.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(['short_text_field.tests'])
    sys.exit(bool(failures))