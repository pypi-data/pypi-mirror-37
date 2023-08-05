"""Fully automated luxury Aptivate command line interface."""

from setuptools import find_packages, setup

dependencies = [
    'ansible',
    'ansible_runner',
    'click',
    'click-datetime',
    'colorama',
    'cookiecutter',
]

with open('README.md', 'r') as handle:
    long_description = handle.read()

setup(
    name='aptivate-cli',
    version='0.0.8',
    url='https://git.coop/aptivate/internal-tools/aptivate-cli',
    license='GPLv3',
    author='Aptivate Hackers',
    author_email='carers+aptivate-cli@aptivate.org',
    description='Fully automated luxury Aptivate command line interface.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'aptivate-cli= aptivate_cli.cli:main',
            'apc = aptivate_cli.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'Intended Audience :: Developers',
    ]
)
