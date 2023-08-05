from setuptools import setup, find_packages
import sys, os

version = '0.21'

requirements = []
if __name__=='__main__':
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt'), 'r') as read_file:
        requirements = list(map(lambda x: x.split()[0], read_file.readlines()))

setup(name='yogasoft',
      version=version,
      description="yogasoft software",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python3',
      author='codertarasvaskiv',
      author_email='codertarasvaskiv@gmail.com',
      url='https://yogasoft.codernetwork.ga',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requirements,
      entry_points={
        'console_scripts': [
            'managepy =  yogasoft:manage',
            ]
        },
      )
