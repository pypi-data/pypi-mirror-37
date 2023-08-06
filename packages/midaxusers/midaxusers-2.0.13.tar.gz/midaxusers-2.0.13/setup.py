import io

from setuptools import find_packages, setup

setup(
    name='midaxusers',
    version='2.0.13',
    url='http://www.midax.com',
    license='BSD',
    maintainer='Midax',
    maintainer_email='alex.r@midax.com',
    description='Midax Users API',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'musersdbcreate = midaxusersutils.manage:create_db',
            'muserstestuser = midaxusersutils.manage:create_test_user'
        ]
    },
    install_requires=[
        'flask',
        'alembic',
        'astroid',
        'attrs',
        'click',
        'colorama',
        'Flask',
        'Flask-HTTPAuth',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'isort',
        'itsdangerous',
        'Jinja2',
        'lazy-object-proxy',
        'Mako',
        'MarkupSafe',
        'mccabe',
        'pluggy',
        'py',
        'pylint',
        'pyodbc',
        'python-dateutil',
        'python-editor',
        'six',
        'SQLAlchemy',
        'Werkzeug',
        'wrapt',
        'cx_Oracle',
    ]  
)