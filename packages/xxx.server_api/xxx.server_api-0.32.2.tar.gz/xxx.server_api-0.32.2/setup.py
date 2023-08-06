import os

from setuptools import setup, find_packages

VERSION = '0.32.2'
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'couchdb-schematics',
    'gevent',
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_redis_sessions',
    'schematics',
    'waitress',
    'boto3',
    'requests',
    'chaussette'
    ]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    ]

entry_points = {
    'paste.app_factory': [
        'main = xxx.server_api:main'
    ]
}

setup(name='xxx.server_api',
      version=VERSION,
      description='xxx',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      namespace_packages=['xxx'],
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points=entry_points
      )
