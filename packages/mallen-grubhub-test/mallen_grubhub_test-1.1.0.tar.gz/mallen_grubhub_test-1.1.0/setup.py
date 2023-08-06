import os
from setuptools import setup, find_packages



readme = 'README.md'
requirements = ['pandas>=0.23.4', 'scikit-learn>=0.20', 'click>=7.0']
python_versions = '>=3.6'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mallen_grubhub_test",
    version = "1.1.0",
    author = "Brenton Mallen",
    author_email = "brentonmallen1@gmail.com",
    description = ("A small module to train and save a classifier."),
    license = "MIT",
    keywords = "model train save",
    url = "https://github.com/brentonmallen1/grubhub_test",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'train = grubhub.train:main'
        ]},
    long_description=read(readme),
    install_requires=requirements,
    python_requires=python_versions,
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
)