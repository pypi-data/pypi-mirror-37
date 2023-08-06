from setuptools import setup

setup(
    name="flask-kit",
    version="0.0.3",
    author="Rysev Alexei",
    author_email="alexeirysev@gmail.com",
    description="Flask extension pack for quick start",
    long_description='Flask-Sqlalchemy, Flask-RESTful extensions config for flask app',
    url="https://bitbucket.org/rysev-a/flask-kit",
    packages=['flask_kit'],
    install_requires=[
        'Flask==1.0.2',
        'SQLAlchemy==1.2.9',
        'Flask-Migrate==2.3.0',
        'Flask-RESTful==0.3.6',
        'Flask-SQLAlchemy==2.3.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
