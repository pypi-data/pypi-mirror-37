import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='sentry_django_settings',
    version='0.4',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Easy Django-Sentry integration via Django settings.',
    long_description=README,
    url='https://gitlab.com/enervee/sentry_django_settings',
    author='Salvatore Lopiparo',
    author_email='salvatore@enervee.com',
    install_requires=[
        'sentry_sdk',
        'gitpython',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
