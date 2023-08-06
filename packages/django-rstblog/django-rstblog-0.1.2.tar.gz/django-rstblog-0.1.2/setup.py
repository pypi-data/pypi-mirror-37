import os
from setuptools import find_packages, setup
from rstblog.version import __version__ as version

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

CLASSIFIERS=[
    'Development Status :: 4 - Beta',  
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 2.0',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]

DEPENDENCIES=[
          'docutils==0.14',
          'Django==2.1.2',
          'django-concurrency==1.4',
          'Markdown==2.6.11',
          'Pygments==2.2.0',
          'python-markdown-math==0.6',
      ],

setup(
    name='django-rstblog',
    version=version,
    packages=find_packages(exclude=("__pycache__",)),
    include_package_data=True,
    license='MIT License',
    description='A Django app to manage a blog driven by articles written using a markup language',
    long_description=README,
    url='https://github.com/l-dfa/django-rstblog',
    author='luciano de falco alfano',
    author_email='ldefalcoalfano@hotmail.com',
    install_requires=DEPENDENCIES,
    classifiers=CLASSIFIERS,
)