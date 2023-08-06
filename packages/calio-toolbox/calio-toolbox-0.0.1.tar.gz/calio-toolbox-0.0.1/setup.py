from distutils.core import setup

setup(
  name='calio-toolbox',
  version='0.0.1',
  author='calio',
  author_email='vipcalio@gmail.com',
  url='https://gitlab.com/calio/toolbox',
  license="MIT",
  long_description="A collections of tools and libraries by calio",
  packages=['toolbox'],
  scripts=['bin/list']
)