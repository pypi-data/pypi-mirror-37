import codecs
import os
import sys

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='flask-foreignkey',
    version='0.2',
    url='https://github.com/ShakeM/flask-foreignkey',
    license='MIT',
    author='Jonathan Nuance',
    author_email='jonathan.nuance@outlook.com',
    description='Use class decorator to add foreign keys.',
    long_description=read("README.txt"),
    py_modules=['flask_foreignkey'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    packages=find_packages(),
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
