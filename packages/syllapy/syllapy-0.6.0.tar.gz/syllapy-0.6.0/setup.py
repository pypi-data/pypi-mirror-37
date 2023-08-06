# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['syllapy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'syllapy',
    'version': '0.6.0',
    'description': 'Calculate syllable counts for English words.',
    'long_description': "SyllaPy\n=======\n\n[![PyPI version](https://badge.fury.io/py/syllapy.svg)](https://badge.fury.io/py/syllapy)\n\n[![Build Status](https://travis-ci.org/mholtzscher/syllapy.svg?branch=master)](https://travis-ci.org/mholtzscher/syllapy)\n\nCalculate syllable counts for English words.\n\n\nInstallation\n------------\n\n``` {.sourceCode .python}\npip install syllapy\n```\n\nUsage\n-----\n\n``` {.sourceCode .python}\nimport syllapy\ncount = syllapy.count('additional')\n```\n\n",
    'author': 'Michael Holtzscher',
    'author_email': 'mholtz@protonmail.com',
    'url': 'https://github.com/mholtzscher/syllapy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
