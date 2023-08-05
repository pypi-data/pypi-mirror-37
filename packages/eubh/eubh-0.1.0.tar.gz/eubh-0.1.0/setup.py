# -*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
from src.eubh.config import VERSION

setup(name='eubh',
      version=VERSION,
      description='eub client help',
      keywords='eub client help',
      author='eubchain',
      author_email='service@eubchain.com',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'click', 'requests', 'azure', 'netifaces', 'apscheduler', 'docker', 'rarfile', 'ws4py', 'PyJWT', 'tqdm',
          'wget', 'zipfile', 'sseclient-py', 'urllib3', 'pick', 'websocket', 'psutil'
      ],
      entry_points={
          'console_scripts': [
              'eubh=src.__main__:main'
          ]
      }
      )
