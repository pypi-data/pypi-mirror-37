from setuptools import setup

setup(name='qbit',
      version='0.2.6',
      description='Client Library for 1QBit Quantum Cloud',
      url='http://1qbit.com',
      author='1 QB Information Technologies',
      author_email='info@1qbit.com',
      license='APLv2',
      packages=['qbit'],
      install_requires=[
          'requests',
          'grpcio-tools',
          'googleapis-common-protos'
      ],
      data_files=[('qbit',['ca.pem'])],
      zip_safe=False)
