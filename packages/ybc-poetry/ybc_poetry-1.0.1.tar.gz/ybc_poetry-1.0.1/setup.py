from distutils.core import setup


setup(
  name='ybc_poetry',
  packages=['ybc_poetry'],
  package_data={'ybc_poetry': ['data/*', '*.py']},
  version='1.0.1',
  description='Poetry search',
  long_description='Poetry search',
  author='hurs',
  author_email='hurs@fenbi.com',
  keywords=['pip3', 'python3', 'python', 'Poetry search'],
  license='MIT',
)
