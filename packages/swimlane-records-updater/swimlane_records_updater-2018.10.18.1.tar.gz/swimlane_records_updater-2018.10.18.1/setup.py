from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="swimlane_records_updater",
    version="2018.10.18.1",
    author="Jeremy M Crews",
    author_email="jeremy.m.crews@gmail.com",
    description="Common Record Updater for Swimlane apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeremymcrews/swimlane_record_updater",
    packages=find_packages(),
    install_requires=[
        'swimlane',
        'ConfigParser',
        'slackclient'
    ],
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)