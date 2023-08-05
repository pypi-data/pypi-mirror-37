from setuptools import setup, find_packages
setup(
  name = 'static_data',
  packages = find_packages(),
  version = '0.1.0',
  description = 'Library to easily handles ddragon ressources files for League of Legends',
  author = 'Canisback',
  author_email = 'canisback@gmail.com',
  url = 'https://github.com/Canisback/static-data',
  keywords = ['Riot API', 'python','static-data'],
  classifiers = [],
  install_requires=[
    "requests"
  ],
)
