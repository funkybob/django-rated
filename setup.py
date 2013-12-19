from setuptools import setup, find_packages

setup(
    name='django-rated',
    version='1.0.3',
    description='A rate limiting middleware for Django',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/django-rated',
    keywords=['django', 'api',],
    packages = find_packages(exclude=['test.*']),
    zip_safe=False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    requires = [
        'Django (>=1.5)',
        'redis (>=2.7.2)',
    ],
)
