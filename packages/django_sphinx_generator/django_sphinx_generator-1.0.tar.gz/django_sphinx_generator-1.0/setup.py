
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_sphinx_generator',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Generate a sphinx documentation tree of django models and other classes.',
    long_description=README,
    url='https://www.github.com/codento/django-sphinx-generator',
    author='Ilkka Tuohela',
    author_email='ilkka.tuohela@codento.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
