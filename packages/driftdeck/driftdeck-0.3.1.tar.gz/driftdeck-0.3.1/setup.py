#!/usr/bin/env python3

from io import open
from setuptools import setup, find_packages


def long_description():
    with open('README.md', 'r') as fd:
        return fd.read()


setup(
    name='driftdeck',
    version='0.3.1',
    author='Ricardo Band',
    author_email='email@ricardo.band',
    description='Drift Deck eats markdown files and spits out beautiful slides directly into your browser.',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/XenGi/driftdeck',
    packages=find_packages(exclude=['tests', ]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications',
        'Topic :: Education',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Text Processing :: Markup',
    ],
    install_requires=['markdown', 'docopt'],
    license='MIT',
    keywords='markdown slides browser',
    package_data={
        '': ['*.css', '*.html'],
    },
    python_requires='>=3.3',
    entry_points={
        'console_scripts': [
            'driftdeck = driftdeck.core:start',
        ],
    },
)

