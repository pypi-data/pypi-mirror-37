from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='commandtax',
    packages=find_packages(),
    version='0.0.8',
    description='Commandtax is a driver which uses clean, one line commands to standardize and simplify working with automation, API\'s, and drivers.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shawn Clake',
    author_email='shawn.clake@gmail.com',
    url='https://github.com/Apitax/Commandtax',
    keywords=['restful', 'api', 'commandtax', 'scriptax', 'apitax', 'drivers', 'plugins'],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'click',
        'apitaxcore==3.0.6',
    ],
)
