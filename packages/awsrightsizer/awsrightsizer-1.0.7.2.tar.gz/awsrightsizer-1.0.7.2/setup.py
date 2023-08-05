# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['rightsizer']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0']

entry_points = \
{'console_scripts': ['rightsizer = rightsizer.main:main']}

setup_kwargs = {
    'name': 'awsrightsizer',
    'version': '1.0.7.2',
    'description': 'A Python3 tool to help you determine the correct instance types to use for your running EC2/RDS instances.',
    'long_description': '|made-with-python| |PyPI pyversions| |PyPI version| |Maintenance| |Open\nSource Love png2|\n\nAWS EC2/RDS Instance Right-Sizer\n================================\n\nThis tool is designed and written in Python 3.6.5 to help you determine\nthe right AWS EC2/RDS instance type for your servers based on historical\nusage.\n\nUsage:\n------\n\n::\n\n    usage: rightsizer.py [-h] [-p PROFILE] [-k ACCESSKEY] [-s SECRETKEY]\n                         [-r REGION] [-t THRESHOLD THRESHOLD] [-q QUERY]\n                         [-o OUTPUT] [-e] [-d]\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      -p PROFILE, --profile PROFILE\n                            AWS Credentials Profile\n      -k ACCESSKEY, --access-key ACCESSKEY\n                            AWS Access Key Id\n      -s SECRETKEY, --secret-key SECRETKEY\n                            AWS Secret Access Key\n      -r REGION, --region REGION\n                            AWS Region\n      -t THRESHOLD THRESHOLD, --threshold THRESHOLD THRESHOLD\n                            The Cloudwatch [average, max] CPU usage threshold\n      -q QUERY, --query-config QUERY\n                            The amount of [days, period] to query Cloudwatch for\n      -o OUTPUT, --output OUTPUT\n                            The name/location of the csv file to output\n      -e, --ec2-only        Run this tool against EC2 Instances only\n      -d, --rds-only        Run this tool against RDS Instances only\n\nInstallation:\n-------------\n\nA pip package is available for this tool. This is the recommended way to\ninstall and run the tool. Download and run the tool using the steps\nbelow:\n\n1. ``python3 -m pip install awsrightsizer --user``\n\n2. ``rightsizer [OPTIONS]``\n\nUpgrading\n---------\n\nUpgrading is easy as well with pip, simply issue the following commands:\n\n1. ``python3 -m pip install awsrightsizer --upgrade --user``\n\n2. ``rightsizer [OPTIONS]``\n\nSource Installation:\n--------------------\n\nThis tool is best run in a virtual environment. You may need to install\na virtual environment tool such as python3-venv or python3-virutalenv\nvia your package manager and/or install one via pip by running\n``pip install virtualenv --user``.\n\n1. ``git clone https://github.com/gregoryjordanm/awsrightsizer.git``\n\n2. ``cd ./awsrightsizer``\n\n3. ``python3 -m venv venv`` or ``virtualenv -p python3 venv``\n\n4. ``. ./venv/bin/activate``\n\n5. ``pip install -r requirements``\n\n6. ``python rightsizer.py [OPTIONS]``\n\nRunning Example:\n----------------\n\nLets assume for a second that you have already installed the AWS CLI\ntools for your distribution…\n\nLets also assume that you have already run the ``aws configure`` command\nand have a profile named “dev” on your system that you have already\ntested and is functioning :)\n\nTo run this tool with your working profile, simply do the following:\n\n``rightsizer -p dev``\n\nThe tool will output a “report\\_\\ *date*.csv” file in the directory you\nran it in.\n\nLets now assume that you hate my report name, simply run:\n\n``rightsizer -p dev -o your_awesome_new_csv.csv``\n\nThe tool will now use your_awesome_new_csv.csv is the output file.\n\nIf you don’t have an AWS profile set up for some reason (it really does\nmake life easier), then you can use the -k, -s. and -r flags to provide\nthe necessary info.\n\n``rightsizer -k XXXXXXXXXXXX -s XXXXXXXXXXXXXXXXXXXXXXXX -r us-east-1``\n\nIf you don’t want to have the tool pull 30 days worth of data, or if you\ndon’t want the data periods to be 30 minutes, use the -q flag like so:\n\n``rightsizer -p dev -q 15,900``\n\nThis will tell the tool to query 15 days at 15 minute intervals.\n\nTo run against just your EC2 assets, just issue the -e flag.\n\nTo run against just your RDS assets, just issue the -d flag.\n\nIf you are running this via the source, you will need to add\n``python rightsizer.py`` to your command instead of just ``rightsizer``.\n\nLet me know if you find bugs :)\n\nAttribution:\n~~~~~~~~~~~~\n\nThis tools is loosely based on the\n`awsstats <https://github.com/FittedCloud/awsstats>`__ tool by\n`FittedCloud <https://www.fittedcloud.com/>`__.\n\n.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg\n   :target: https://www.python.org/\n.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/ansicolortags.svg\n   :target: https://pypi.python.org/pypi/ansicolortags/\n.. |PyPI version| image:: https://badge.fury.io/py/awsrightsizer.svg\n   :target: https://badge.fury.io/py/awsrightsizer\n.. |Maintenance| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg\n   :target: https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity\n.. |Open Source Love png2| image:: https://badges.frapsoft.com/os/v2/open-source.png?v=103\n   :target: https://github.com/ellerbrock/open-source-badges/\n',
    'author': 'Jordan Gregory',
    'author_email': 'jordan@gregory-dev.io',
    'url': 'http://www.gregory-dev.io/awsrightsizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
