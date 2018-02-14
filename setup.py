import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))

setup(
    name='django-pipes-blog',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='',
    description='Simple blogging app for the Django framework',
    long_description=README,
    url='https://github.com/arpiper/django-pipes-blog',
    author='Andrew Piper',
    author_email='',
    classifiers=[
        'Environment :: Web Development',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
