# this is your project's setup.py script
#python setup.py sdist upload

import os
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig

from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

class register(register_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')

class upload(upload_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')
setup(name='securefile',
      version='1.0.0',
      description='A python package for hybrid file encryption and decryption. securefile is for n-layer file encryption. This package provides a basic two-way encryption algorithm for a file. It supports approximately all kind of file encoding. The package provides RSA, DES, AES and Shift Cipher and base64 algorithm for file encoding and decoding.',
      author='Prashant Kumar, Pamela Banerjee',
      author_email='kr.prashant94@gmail.com',
      url='https://github.com/Krprashant94/securefile',
      license='MIT',
      long_description = read('README'),
      packages=['securefile'],
      zip_safe=True,
      cmdclass={
        'register': register,
        'upload': upload,
    })