from setuptools import setup
from gladepaypython import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='gladepaypython',
    version=version.__version__,
    description='Python wrapper for Gladepay API',
    long_description=long_description,
    url='https://gitlab.com/gladepay-apis/gladepay-python',
    author=version.__author__,
    author_email='light@yottabitconsulting.com',
    license=version.__license__,
    install_requires=['requests', 'nose2'],
    test_suite='nose.collector',
    tests_require=['nose2'],
    packages=['gladepaypython'],
    zip_safe=False
    )
