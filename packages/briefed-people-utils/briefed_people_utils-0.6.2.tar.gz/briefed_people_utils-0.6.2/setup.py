from setuptools import find_packages,setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='briefed_people_utils',
    version='0.6.2',
    description='Tools to support collect and send publically available data to Briefed.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://Briefed.eu',
    author='Marek Zaremba-Pike',
    author_email='marekzp@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'bs4',
        'lxml',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)