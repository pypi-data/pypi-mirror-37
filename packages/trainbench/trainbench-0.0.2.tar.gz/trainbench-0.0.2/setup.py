from setuptools import setup, find_packages


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='trainbench',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    version='0.0.02',
    description='A tool for training deep learning cross validation training.',
    author='danfergo',
    entry_points={
        'console_scripts': [
            'trainbench = trainbench.__main__:main'
        ],
    },
    # scripts=['bin/lidaco'],
    author_email='e-windlidar@googlegroups.com',
    url='https://github.com/danfergo/trainbench',  # use the URL to the github repo
    keywords=['deep', 'learning', 'cross', 'validation'],  # arbitrary keywords
    classifiers=[],
    install_requires=[
    ]
)
