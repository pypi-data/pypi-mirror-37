from setuptools import setup, find_packages

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mfetcher',
    version='0.1',
    author='Aurel Megnigbeto',
    author_email='shiftsh@protonmail.ch',
    description='A simple cli tool to download mangas scan from the internet scan provider to your local file system',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sh1ftsh/mangas-scan-fetch',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts':['mfetcher=mfetcher.command_line:main']
    },
    zip_safe=False)
