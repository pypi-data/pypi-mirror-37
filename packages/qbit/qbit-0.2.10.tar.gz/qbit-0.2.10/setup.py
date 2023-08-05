from setuptools import setup

setup(name='qbit',
      version='0.2.10',
      description='Client Library for 1QBit Quantum Cloud',
      url='http://1qbit.com',
      author='1 QB Information Technologies',
      author_email='info@1qbit.com',
      license='APLv2',
      packages=['qbit'],
      package_data={  # Optional
        'qbit': ['ca.pem'],
      },
      install_requires=[
          'requests',
          'grpcio-tools',
          'googleapis-common-protos'
      ],
      zip_safe=False)
