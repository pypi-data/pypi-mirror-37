try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import find_packages

setup(name='liveline',
      version='1.1',
      description='Python live trading framework',
      author='Daniel Wang',
      author_email='danielwpz@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['tests*']),
      install_requires=[
          'arrow',
          'maya',
          'pandas',
          'pymongo',
          'pytz',
          'schedule',
          'flask',
          'pandas-market-calendars'
      ],
      zip_safe=False)
