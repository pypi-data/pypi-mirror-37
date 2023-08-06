from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='scriptaxstd',
    packages=find_packages(),
    version='0.0.5',
    description='The Standard Library is a driver which provides lots of additional functionality to complement the Scriptax driver.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shawn Clake',
    author_email='shawn.clake@gmail.com',
    url='https://github.com/Apitax/StandardLibrary',
    keywords=['restful', 'api', 'commandtax', 'scriptax', 'apitax', 'drivers', 'plugins'],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'click',
        'apitaxcore==3.0.6',
        'commanndtax==0.0.8',
        'scriptax==0.0.4',
    ],
)
