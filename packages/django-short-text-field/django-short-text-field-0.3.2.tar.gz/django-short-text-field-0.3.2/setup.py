import os
from pathlib import Path
from setuptools import find_packages, setup

path = Path(__file__)
README = (path.parent/'README.md').read_text()
os.chdir(path.parent.resolve())

setup(
    name='django-short-text-field',
    version='0.3.2',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A Django app which adds a ShortTextField model field, which'
                'is like a TextField in the database but uses the TextInput'
                'rather than the Textarea widget in forms.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://www.example.com/',
    author='Andrew Foote',
    author_email='footeandrew1@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)