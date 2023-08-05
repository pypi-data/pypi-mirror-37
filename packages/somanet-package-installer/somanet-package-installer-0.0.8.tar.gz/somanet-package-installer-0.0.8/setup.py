import setuptools

with open('README.md', 'r') as fh:
  long_description = fh.read()

setuptools.setup(
  name='somanet-package-installer',
  version='0.0.8',
  author='Marko Sanković',
  author_email='msankovic@synapticon.com',
  description='Install SOMANET motion drive package to an EtherCAT slave',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/synapticon/somanet-package-installer',
  license='MIT',
  packages=setuptools.find_packages(),
  classifiers=(
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux'
  ),
  scripts=['somanet-package-installer']
)
