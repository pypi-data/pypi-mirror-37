from distutils.core import setup


setup(
  name='ybc_animal',
  packages=['ybc_animal'],
  package_data={'ybc_animal': ['data/*', '*.py', 'test.jpg']},
  version='2.0.7',
  description='Recognition Image Animal',
  long_description='Recognition Image Animal',
  author='hurs',
  author_email='hurs@fenbi.com',
  keywords=['pip3', 'python3', 'python', 'Recognition Image Animal'],
  license='MIT',
  install_requires=['requests', 'ybc_config']
)
