# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['rightsizer']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0', 'click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['rightsizer = rightsizer.main:main']}

setup_kwargs = {
    'name': 'awsrightsizer',
    'version': '1.1.2',
    'description': 'A Python3 tool to help you determine the correct instance types to use for your running EC2/RDS instances.',
    'long_description': '[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/) [![PyPI version](https://badge.fury.io/py/awsrightsizer.svg)](https://badge.fury.io/py/awsrightsizer) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity) [![Open Source Love png2](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)\n\n# AWS EC2/RDS Instance Right-Sizer\n\nThis tool is designed and written in Python 3.6.5 to help you determine the right AWS EC2/RDS instance type for your servers based on historical usage.\n\n## Usage:\n\n```\nuUsage: rightsizer.py [OPTIONS]\n\n  rightsizer takes user input and provides an output CSV of suggestions.\n\nOptions:\n  -p, --profile TEXT             Your AWS Credentials Profile.\n  -k, --access-key TEXT          Your AWS Access Key ID.\n  -s, --secret-key TEXT          Your AWS Secret Access Key ID.\n  -r, --region TEXT              The AWS Region to query.\n  -t, --threshold INTEGER...     The Cloudwatch [average, max] CPU usage\n                                 threshold.\n  -q, --query-config INTEGER...  The amount of [days, period] to query\n                                 Cloudwatch for.\n  -o, --output TEXT              The Name/Location of the file to output.\n  -e, --ec2-only\n  -d, --rds-only\n  -v, --verbose\n  -h, --help                     Print help message\n\n```\n\n## Installation:\nA pip package is available for this tool. This is the recommended way to install and run the tool. Download and run the tool using the steps below:\n\n1. ```python3 -m pip install awsrightsizer --user```\n\n2. ```rightsizer [OPTIONS]```\n\n## Upgrading\nUpgrading is easy as well with pip, simply issue the following commands:\n\n1. ```python3 -m pip install awsrightsizer --upgrade --user```\n\n2. ```rightsizer [OPTIONS]```\n\n## Source Installation:\nThis tool is best run in a virtual environment. You may need to install a virtual environment tool such as python3-venv or python3-virutalenv via your package manager and/or install one via pip by running ```pip install virtualenv --user```.\n\n1. ```git clone https://github.com/gregoryjordanm/awsrightsizer.git```\n\n2. ```cd ./awsrightsizer```\n\n3. ```python3 -m venv venv``` or ```virtualenv -p python3 venv```\n\n4. ```. ./venv/bin/activate```\n\n5. ```pip install -r requirements```\n\n6. ```python rightsizer.py [OPTIONS]```\n\n## Running Example:\n\nLets assume for a second that you have already installed the AWS CLI tools for your distribution...\n\nLets also assume that you have already run the ```aws configure``` command and have a profile named "dev" on your system that you have already tested and is functioning :)\n\nTo run this tool with your working profile, simply do the following:\n\n```rightsizer -p dev```\n\nThe tool will output a "report_*date*.csv" file in the directory you ran it in.\n\nLets now assume that you hate my report name, simply run:\n\n```rightsizer -p dev -o your_awesome_new_csv.csv```\n\nThe tool will now use your_awesome_new_csv.csv is the output file.\n\nIf you don\'t have an AWS profile set up for some reason (it really does make life easier), then you can use the -k, -s. and -r flags to provide the necessary info.\n\n```rightsizer -k XXXXXXXXXXXX -s XXXXXXXXXXXXXXXXXXXXXXXX -r us-east-1```\n\nIf you don\'t want to have the tool pull 30 days worth of data, or if you don\'t want the data periods to be 30 minutes, use the -q flag like so:\n\n```rightsizer -p dev -q 15,900```\n\nThis will tell the tool to query 15 days at 15 minute intervals.\n\nTo run against just your EC2 assets, just issue the -e flag.\n\nTo run against just your RDS assets, just issue the -d flag.\n\nIf you are running this via the source, you will need to add ```python rightsizer.py``` to your command instead of just ```rightsizer```. \n\nLet me know if you find bugs :)\n\n### Attribution:\n\nThis tools is loosely based on the [awsstats](https://github.com/FittedCloud/awsstats) tool by [FittedCloud](https://www.fittedcloud.com/).\n\n',
    'author': 'Jordan Gregory',
    'author_email': 'jordan@gregory-dev.io',
    'url': 'https://github.com/Gregory-Development/awsrightsizer/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
