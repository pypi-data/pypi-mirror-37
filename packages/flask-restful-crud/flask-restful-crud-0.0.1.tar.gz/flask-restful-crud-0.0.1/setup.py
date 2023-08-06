from setuptools import setup

setup(
    name="flask-restful-crud",
    version="0.0.1",
    author="Rysev Alexei",
    author_email="alexeirysev@gmail.com",
    description="Bootstrap classes for flask-restful",
    long_description='Helpers for quick start rest api',
    url="https://bitbucket.org/rysev-a/flask-restful-crud",
    packages=['flask_restful_crud'],
    install_requires=[
        'Flask==1.0.2',
        'Flask-RESTful==0.3.6',
        'SQLAlchemy==1.2.9'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
