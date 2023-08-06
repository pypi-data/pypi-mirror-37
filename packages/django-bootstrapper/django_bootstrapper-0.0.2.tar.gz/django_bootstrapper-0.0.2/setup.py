import codecs
from setuptools import setup

def readme():
    with codecs.open('README.md') as f:
        return f.read()

setup(
    name='django_bootstrapper',
    version='0.0.2',
    description='A simple bootstrapper for django applications',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='http://github.com/contraslash/django-bootstrapper',
    keywords='django bootstrapping tool',
    author='contraslash S.A.S.',
    author_email='ma0@contraslash.com',
    classifiers=[ 
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    install_requires=['gitpython>=2.1'],
    packages=['django_bootstrapper'],
    scripts=['django_bootstrapper/bin/django-bootstrapper.py'],
    zip_safe=False,
    include_package_data=True,
    project_urls={  
        'Bug Reports': 'https://github.com/contraslash/django-bootstrapper/issues',
        'Source': 'https://github.com/contraslash/django-bootstrapper',
        'Contraslash': 'https://contraslash.com/'
    },
)
 