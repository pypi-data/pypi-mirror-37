import os
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig

from setuptools import setup, find_packages


class register(register_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')


class upload(upload_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')


# from distutils.core import setup
setup(
    name='sparkworks',
    packages=['sparkworks'],
    version='2.0.0',
    description='A client library for the sparkworks api',
    author='SparkWorks ITC',
    author_email='info@sparkwokrs.net',
    url='http://sparkworks.net',  # use the URL to the github repo
    download_url='https://github.com/SparkWorksnet/client',  # I'll explain this in a second
    keywords=['client', 'sparkworks'],  # arbitrary keywords
    include_package_data=True,
    classifiers=[],
    cmdclass={
        'register': register,
        'upload': upload,
    },
    install_requires=['requests']
)
