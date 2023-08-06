from setuptools import setup, find_packages
from django_cognito import __version__ as version

setup(
    name='django_cognito',
    version=version,
    packages=find_packages(),
    url='https://github.com/Olorin92/django_cognito',
    license='',
    author='Alex Plant',
    author_email='alex.c.plant@gmail.com',
    description='Library for allowing the use of AWS Cognito security in Django projects',
    install_requires=[
        "asn1crypto==0.24.0",
        "boto3==1.9.0",
        "botocore==1.12.0",
        "cryptography==2.3.1",
        "Django==2.1.2",
        "djangorestframework==3.8.2",
        "idna==2.7",
        "PyJWT==1.6.4",
        "python-dateutil==2.7.3",
        "urllib3==1.23",
    ]
)
