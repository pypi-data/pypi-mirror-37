import os
import json
from setuptools import setup, find_packages

folder = 'data/builds'
if not os.path.exists(folder):
    os.makedirs(folder)

# Create levels.json file
if not os.path.exists('data/levels.json'):
    levels = [1, 4, 7, 10, 13, 16, 20]
    with open('data/levels.json', 'w') as fp:
        json.dump(levels, fp)

with open('requirements.txt') as fp:
    required = fp.read().splitlines()

setup(
    install_requires=required,
    name='heroes_build_scrapper',
    version='1.1',
    author='Gabriel Cruz',
    author_email=('gabs.oficial98@gmail.com'),
    packages=find_packages('src'),
    package_dir={"": "src"},
    description='A library for scraping builds for Heroes of the Storm heroes.')