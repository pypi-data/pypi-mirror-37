#from distutils.core import setup
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ECSU_Midterm_Proj', # a unique name for PyPI
    version='0.2',
    description='Extracts HTML data with python regex and convert the data to a csv file',
    author='Disaiah Bennett',
    author_email='dlbennett365@ecsu.edu',
    url='https://github.com/dislbenn', # http://location or https://location
    install_requires=requirements,
    packages=['myFormat', 'myFormat/sub', ], # packages and subpackages containing .py file
    package_dir={'':'src'},
    package_data={'myFormat':['other/*']}, # other needed files will be installed for user
    scripts=['src/extract',], # the executable files will be installed for user
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README').read(),
    # more meta-data for repository
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: X11 Applications :: GTK',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Topic :: Desktop Environment',
      'Topic :: Text Processing :: Fonts'
      ],
)
