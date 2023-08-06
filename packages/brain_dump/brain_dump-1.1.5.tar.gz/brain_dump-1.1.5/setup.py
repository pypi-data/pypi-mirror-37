# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['brain_dump', 'brain_dump.cli', 'brain_dump.parsers']

package_data = \
{'': ['*']}

install_requires = \
['pydot', 'pyparsing']

entry_points = \
{'console_scripts': ['graphviz_md2png = brain_dump.cli.graphviz_md2png:main',
                     'wisemapping_md2xml = '
                     'brain_dump.cli.wisemapping_md2xml:main',
                     'wisemapping_wxml2xml = '
                     'brain_dump.cli.wisemapping_wxml2xml:main']}

setup_kwargs = {
    'name': 'brain-dump',
    'version': '1.1.5',
    'description': 'Tools to generate mindmaps compatible from markdown-like text files, either as PNG with graphviz or as wisemapping-compatible XMLs',
    'long_description': "[![pypi\\_version\\_img](https://img.shields.io/pypi/v/brain_dump.svg?style=flat)](https://pypi.python.org/pypi/brain_dump) [![pypi\\_license\\_img](https://img.shields.io/pypi/l/brain_dump.svg?style=flat)](https://pypi.python.org/pypi/brain_dump) [![travis\\_build\\_status](https://travis-ci.org/Lucas-C/brain_dump.svg?branch=master)](https://travis-ci.org/Lucas-C/brain_dump) [![snyk\\_deps\\_status](https://snyk.io/test/github/lucas-c/brain_dump/badge.svg)](https://snyk.io/test/github/lucas-c/brain_dump)\n\nTools to generate mindmaps compatible from markdown-like text files,\neither as PNG with graphviz or as wisemapping-compatible XMLs.\n\nA viewer for those can be found here: <https://github.com/Lucas-C/wisemapping-mindmap-viewer>\n\nAlso include a [Twilio](<https://www.twilio.com>) webhook that can\nreceive updates for such markdown-like mindmap files, stored in git.\n\nFor more information, I wrote some [blog posts](<https://chezsoi.org/lucas/blog/tag/mindmap/>)\nexplaining the role of those scripts.\n\nUsage\n=====\n\n    wisemapping_md2xml examples/welcome.md > welcome.xml\n\n    graphviz_md2png examples/seasons.md\n\nDeployment\n==========\n\n`upstart` job using `pew` & `uwsgi`: `/etc/init/brain_dump.conf`\n\n    start on startup\n\n    script\n        set -o errexit -o nounset -o xtrace\n        cd /path/to/git/dir\n        exec >> upstart-stdout.log\n        exec 2>> upstart-stderr.log\n        date\n        APP_SCRIPT=$(dirname $(pew-in brain_dump python -c 'import brain_dump; print(brain_dump.__file__)'))/twilio_webhook_gitdb_app.py\n        LANG=fr_FR.UTF-8 pew-in brain_dump uwsgi --buffer-size 8000 --http :8087 --manage-script-name --mount /webhook=$APP_SCRIPT\n    end script\n\nChangelog\n=========\n\n<https://github.com/Lucas-C/brain_dump/blob/master/CHANGELOG.md>\n\nContributing\n============\n\n    pip install -r dev-requirements\n    pre-commit install\n\nThe 2nd command install the [pre-commit hooks](http://pre-commit.com)\n\nTo only execute a single unit test:\n\n    py.test -k 'test_topic_from_line[toto-expected_topic0]'\n",
    'author': 'Lucas Cimon',
    'author_email': None,
    'url': 'http://github.com/Lucas-C/brain_dump',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
