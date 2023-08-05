#!/usr/bin/env python

from setuptools import setup
import pymc_learn_sphinx_theme

setup(name='pymc_learn_sphinx_theme',
      version=pymc_learn_sphinx_theme.__version__,
      url='https://github.com/pymc-learn/pymc-learn-sphinx-theme/',
      license='BSD',
      author='Pymc-learn Developers',
      description='Pymc-learn theme for Sphinx',
      long_description=open('README.rst').read(),
      zip_safe=False,
      packages=['pymc_learn_sphinx_theme'],
      package_data={'pymc_learn_sphinx_theme': [
          'theme.conf',
          '*.html',
          'static/css/*.css',
          'static/images/*.svg',
          'static/images/*.png',
          'static/js/*.js',
          'static/font/*.*'
      ]},
      include_package_data=True,
      # http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
      entry_points = {
          'sphinx.html_themes': [
              'pymc_learn_sphinx_theme = pymc_learn_sphinx_theme',
          ]
      },
      install_requires=open('requirements.txt').read().strip().split('\n'),
)
