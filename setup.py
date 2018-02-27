import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
VERSION = open(os.path.join(BASEDIR, 'VERSION')).read().strip()
REQUIREMENTS = []
DEPENDENCY_LINKS = []

with open(os.path.join(BASEDIR, 'requirements.pip')) as fp:
    lines = fp.readlines()
    for line in lines:
        line = line.strip()
        if ("http://" in line or "https://" in line or "ssh://" in line) and "#egg=" in line:
            parts = line.split("#egg=")
            REQUIREMENTS.append(parts[-1])
            DEPENDENCY_LINKS.append(line)
        elif len(line) and line[0] != "#" and line[0] != "-":
            REQUIREMENTS.append(line)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(BASEDIR))


setup(
    name='salt-aws-boto3',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    description='Use boto3 for AWS orchestration with Salt.',
    long_description='Use boto3 for AWS orchestration with Salt.',
    url='https://github.com/intuitivetechnologygroup/salt-aws-boto3',
    author='meganlkm',
    author_email='devops@intuitivetech.com',
    install_requires=REQUIREMENTS,
    dependency_links=DEPENDENCY_LINKS,
    keywords=[
        'aws',
        'saltstack'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities'
    ]
)
