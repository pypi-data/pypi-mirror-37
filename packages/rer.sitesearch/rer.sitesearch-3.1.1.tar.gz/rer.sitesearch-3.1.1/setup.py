from setuptools import setup, find_packages
import os

version = '3.1.1'

tests_require = ['plone.app.testing',
                 'selenium>=2.0a5']

setup(name='rer.sitesearch',
      version=version,
      description="A product that change the base site search of Plone with some new features.",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        ],
      keywords='',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.net',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rer'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require={
          'test': tests_require,
      },
      install_requires=[
          'setuptools',
          # 'plone.app.search', removed on P5
          'plone.api',
      ],
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
