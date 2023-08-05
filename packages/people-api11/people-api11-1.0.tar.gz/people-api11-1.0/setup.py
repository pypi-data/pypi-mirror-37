from setuptools import setup, find_packages

setup(
    name='people-api11',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask==1.0.2',
        'flask_restful==0.3.6',
        'flask_script==2.0.6',
        'flask_migrate==2.1.1',
        'marshmallow==2.14.0',
        'flask_sqlalchemy==2.3.2',
        'flask_marshmallow==0.8.0',
        'marshmallow-sqlalchemy==0.13.2',
        'psycopg2==2.7.3.2',
        'flask_paginate==0.5.0',
        'pymongo==3.6.0',
        'gunicorn==19.9.0'
    ]
    
)