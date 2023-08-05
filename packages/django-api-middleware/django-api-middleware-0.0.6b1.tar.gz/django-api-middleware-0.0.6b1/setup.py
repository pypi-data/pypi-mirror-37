import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-api-middleware',
    version='0.0.6b1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Un middleware que agrega un token a cada request y response entre microservicios de los que se tiene propiedad.',
    long_description=README,
    url='https://www.example.com/',
    author='',
    author_email='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['Django>2', 'pyjwt>=1.6.0', 'mock>=2.0.0', 'requests>2', 'ua-parser>=0.8.0', 'psycopg2-binary>=2.7', 'djangorestframework>=3.8.2', 'djangorestframework-jsonapi>=2.4.0', 'djangorestframework-queryfields>=1.0.0']
)
