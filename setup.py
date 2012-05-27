from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='borobudur',
      version=version,
      description="Python web framework based on pyramid and backbone.js",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          "prambanan",
          "pyramid",
          "colander",
          "webassets",
      ],
      entry_points="""
      # -*- Entry points: -*-
      [prambanan.provider]
      borobudur = borobudur.prambanan_provider:BorobudurPrambananProvider
      [pyramid.scaffold]
      borobudur_mongo=borobudur.scaffolds:MongoProjectTemplate
      """,
      )
