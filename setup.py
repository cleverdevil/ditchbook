# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='ditchbook',
    version='0.1.0',
    description='Migrate a Facebook JSON export to your Micropub website.',
    author='Jonathan LaCour',
    author_email='jonathan@cleverdevil.org',
    install_requires=[
        "requests",
        "pytz",
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup']),
)
