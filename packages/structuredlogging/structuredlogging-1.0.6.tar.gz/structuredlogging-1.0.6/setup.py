from setuptools import setup
import setuptools

VERSION = "1.0.6"


DEPENDENCIES = [
    'six',
    'requests'
]

setup( name='structuredlogging',
       version=VERSION,
       description='Python Structured Log CustomFormatter',
       long_description='Python CustomFormatter that generates an opinionated json structured log',
       license='MIT',
       author='Azure CAT E2E',
       author_email='azcate2esupport@microsoft.com',
       url='https://github.com/AzureCATE2E/structuredlogging',
       download_url = 'https://github.com/AzureCATE2E/structuredlogging/blob/master/dist/structuredlogging-1.0.0.tar.gz',
       packages=setuptools.find_packages(),
       include_package_data=True,
       install_requires=DEPENDENCIES,
       zip_safe=False)

