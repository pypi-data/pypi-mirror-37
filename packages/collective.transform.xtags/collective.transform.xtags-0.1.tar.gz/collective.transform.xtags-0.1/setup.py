from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.transform.xtags',
      version=version,
      description="Transform xtags to HTML",
      long_description="Quark Xpress Tags transform",
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing"
        ],
      keywords='',
      author='Espen Moe-Nilssen',
      author_email='espen@medialog.no',
      url='https://github.com/espenmn/collective.transform.xtags',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.transform'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.dexteritytextindexer',
          'plone.autoform',
          'plone.directives.form',
           'plone.supermodel',
          'pypeg2'
          # -*- Extra requirements: -*-
          ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      # The next two lines may be deleted after you no longer need
      # addcontent support from paster and before you distribute
      # your package.
      )
