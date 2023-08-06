import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# setup will be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-bay-polls',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Django app to be used in conducting Web-based polls.',
    long_description=README,
    url='https://github.com/stevemats/django-bay-polls',
    author='Stevemats',
    author_email='contact@stevemats.net',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
     ],
)
