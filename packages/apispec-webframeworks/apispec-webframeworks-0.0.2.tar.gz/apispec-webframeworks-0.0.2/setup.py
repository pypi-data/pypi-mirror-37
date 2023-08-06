# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '0.0.2'


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='apispec-webframeworks',
    version=VERSION,
    description='Web framework plugins for apispec.',
    long_description=read('README.rst'),
    author='Steven Loria',
    author_email='sloria1@gmail.com',
    url='https://github.com/marshmallow-code/apispec-webframeworks',
    packages=find_packages(exclude=('test*', )),
    include_package_data=True,
    install_requires=[
        'apispec[yaml]>=1.0.0b1',
    ],
    extras_require={},
    license='MIT',
    zip_safe=False,
    keywords=(
        'apispec',
        'swagger',
        'openapi',
        'specification',
        'documentation',
        'spec',
        'rest',
        'api',
        'web',
        'flask',
        'tornado',
        'bottle',
        'frameworks',
    ),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    project_urls={
        'Funding': 'https://opencollective.com/marshmallow',
        'Issues': 'https://github.com/marshmallow-code/apispec-webframeworks/issues',
    },
)
