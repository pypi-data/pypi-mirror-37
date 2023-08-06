# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['redditsweeper']

package_data = \
{'': ['*']}

install_requires = \
['ConfigArgParse>=0.13.0,<0.14.0', 'colorama>=0.4.0,<0.5.0', 'praw>=6.0,<7.0']

entry_points = \
{'console_scripts': ['redditsweeper = redditsweeper.app:main']}

setup_kwargs = {
    'name': 'redditsweeper',
    'version': '1.0.1',
    'description': 'Tool for automated removal of old reddit comments.',
    'long_description': '# Reddit Sweeper\n\n![Build Status](https://travis-ci.org/scott-hand/redditsweeper.svg)\n\nThis tool is designed to be an easy-to-use utility to clear out old reddit\ncomments. It aims for simplicity in terms of use as well as configuration. It\ncurrently supports the following features:\n\n* Delete comments and/or submissions\n* Exclude one or more subreddits when search for content to delete\n* Include only a subset of subreddits when searching for content to delete\n* Only delete comments over a given number of days old\n* Save a record of deleted content in an easy to parse JSON file\n\nIt supports Python 2.7, 3.6, 3.7, and PyPy and uses\n[poetry](https://poetry.eustace.io/) for dependency management.\n\n# Installation\n\n## Pip\n\nThe easiest way to install redditsweeper is via Pip, using the following\ncommand:\n\n```\npip install -U redditsweeper\n```\n\n## Poetry\n\nTo install redditsweeper from Github, clone it to your local filesystem, and\nthen from the redditsweeper directory, use:\n\n```\npoetry install\n```\n\n# Usage\n\nOnce installed, a CLI tool called `redditsweeper` should available to use. It\nmay be configured either via command line arguments, a config file, or\nenvironment variables of the form REDDITSWEEPER_<option>.\n\n## Configuring Reddit credentials\n\nFirst, it is necessary to obtain script credentials from reddit. You can set\nthis up easily [here](https://www.reddit.com/prefs/apps/) by doing the\nfollowing:\n\n1. Click "create another app..."\n2. Enter a name of "redditsweeper"\n3. Choose the "script" option\n4. Leave description blank.\n5. Just put "http://127.0.0.1" in each URL field (this are just dummy values\n   and are not used)\n6. Click "create app"\n7. Get the client ID by looking at the line underneath "personal use script"\n8. Get the client secret next to the word "secret"\n\nCreate a copy of [praw.ini.sample](praw.ini.sample) called "praw.ini" and set\nup the values for client ID and secret that you just obtained, as well as\nentering your username and password.\n\nIf your account has multi-factor authentication enabled, you will need to\nsupply redditsweeper with a MFA code each time you run it with the "--mfa"\nparameter in addition to the username and password you set up here.\n\n## Configuring redditsweeper\n\nIf you want to store the settings used, make a copy of\n[redditsweeper.cfg.sample](redditsweeper.cfg.sample) called "redditsweeper.cfg"\nand fill in the options you need. A brief overview of options is as follows:\n\n* **dry** - This is `True` or `False`. If `True`, redditsweeper will operate in\n  dry run mode. It will show you what it would do with each comment or\n  submission, but it will not delete anything.\n* **exclude** - This is a list of subreddits (in the form r/subreddit name)\n  that should be excluded from deletion. Anything found belonging to one of\n  these subreddits will be skipped.\n* **include** - If you want to provide an explicit list of subreddits to target\n  for deletion, provide it here. If nothing is provided, redditsweeper simply\n  considers everything for deletion. Note that if the comment or submission is\n  either in an excluded subreddit or is too new and the `--keep` option was\n  set, it will be skipped regardless of whether it\'s in the include list.\n* **keep** - This is a number of days worth of comments or submissions to keep.\n  Anything newer will be kept no matter what, and anything older will be\n  considered for deletion.\n* **savefile** - If set, a JSON file will be created at the given filename, and\n  it will be updated with the contents of comments and submissions deleted.\n  Any existing savefile will be overwritten.\n* **type** - The type of reddit content to delete. It can be "comment",\n  "submission", or "both".\n* **user** - This controls which section of praw.ini will be used. If you have\n  multiple user accounts and want to switch between deleting content from one\n  account to the other, just overwrite this setting.\n\n# Testing\n\nredditsweeper uses pytest to run tests, with\n[responses](https://github.com/getsentry/responses) used to stub fake responses\nfrom reddit, so no credentials are required for testing. Run the set of tests\nusing the following command:\n\n```\npoetry run py.test --cov=redditsweeper tests/\n```\n\nIt currently supports Python 2.7, 3.6, 3.7, and PyPy, and multi-version tests\ncan be run using:\n\n```\npoetry run tox\n```\n',
    'author': 'Scott Hand',
    'author_email': None,
    'url': 'https://www.github.com/scott-hand/redditsweeper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
