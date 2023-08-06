from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='apitaxdrivers',
    packages=find_packages(),  # this must be the same as the name above
    version='0.0.9',
    description='A set of example and micro drivers which can be used as the basis of more robust API drivers or combined together to form a robust application.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shawn Clake',
    author_email='shawn.clake@gmail.com',
    url='https://github.com/ShawnClake/Apitax',  # use the URL to the github repo
    keywords=['restful', 'api', 'commandtax', 'scriptax', 'apitax', 'drivers', 'plugins'],  # arbitrary keywords
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'requests',
        'python-gitlab',
        'pygithub',
        'gitpython',
        'apitaxcore==3.0.6',
        'commanndtax==0.0.8',
        'scriptax==0.0.4',
    ],
)
