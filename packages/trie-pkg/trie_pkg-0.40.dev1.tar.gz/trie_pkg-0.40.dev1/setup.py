from setuptools import setup
from web import __version__

setup(name='trie_pkg',
      version=__version__,
      description='trie.py: a efficient package for search words using trie tree',
      author='Larry King',
      author_email='1412857955@qq.com',
      maintainer='Scut Emos',
      maintainer_email='emos@scut.edu.cn',
      url=' http://webpy.org/',
      packages=['trie_pkg'],
      long_description="By using this package, call insert function to build search tree, call search function to search a specific word",
      license="Public domain",
      platforms=["any"],
     )

