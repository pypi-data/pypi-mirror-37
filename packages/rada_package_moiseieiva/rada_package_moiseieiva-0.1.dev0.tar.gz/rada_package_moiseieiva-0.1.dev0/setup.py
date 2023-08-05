from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='rada_package_moiseieiva',
      version=version,
      description="rada project",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Irina Moiseieiva',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
            'console_scripts':[
                  'rada = rada_package_moiseieiva.verh_rada:main',
            ]

      },
      )
