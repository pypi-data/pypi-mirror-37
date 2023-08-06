import codecs
from setuptools import setup


def readme():
    with codecs.open('README.md') as f:
        return f.read()

setup(
    name='flask_bootstrapper',
    version='0.0.2',
    description='A simple bootstrapper for flask applications',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='http://github.com/contraslash/flask-bootstrapper',
    keywords='flask bootstrapping tool',
    author='contraslash S.A.S.',
    author_email='ma0@contraslash.com',
    classifiers=[ 
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    install_requires=['gitpython>=2.1', 'django_crud_generator'],
    packages=['flask_bootstrapper'],
    scripts=['flask_bootstrapper/bin/flask-bootstrapper.py'],
    zip_safe=False,
    include_package_data=True,
    project_urls={  
        'Bug Reports': 'https://github.com/contraslash/flask-bootstrapper/issues',
        'Source': 'https://github.com/contraslash/flask-bootstrapper',
        'Contraslash': 'https://contraslash.com/'
    },
)
