from os import path
from setuptools import setup, find_packages
import versioneer


# Read the contents of the README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='context-explorer',
    url='https://gitlab.com/stemcellbioengineering/context-explorer',
    author='Joel Ostblom',
    author_email='joel.ostblom@gmail.com',
    # Needed to actually package something
    packages=find_packages(),
    # scripts=['bin/tile_wells'],
    entry_points={
        'console_scripts': ['ctexplorer=ctexplorer:main']},
    # Needed for dependencies
    install_requires=[
        'matplotlib', 'joblib', 'scikit-learn', 'joblib', 'numpy',
        'pandas', 'shapely', 'matplotlib', 'natsort', 'seaborn', 'scipy',
        'pyqt5', 'scikit-image'],
    # Python version
    python_requires='>=3.6',
    # include_setup_data=True,
    # Package data
    package_data={
        'ctexplorer': [
            'sample-data/ce-sample.csv',
            'icons/ce-icon-keep-white.ico',
            'icons/ce-icon-keep-white.png']},
    # Automatic version number
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    # The license can be anything you like
    license='BSD-3',
    description='''A tool that facilitates analyses of data extracted from
        microscope images of cells''',
    # Inclide readme in markdown format, GFM markdown style by defaul
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
