# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['toasts', 'toasts.clients']

package_data = \
{'': ['*'], 'toasts': ['data/*', 'data/icons/*']}

install_requires = \
['confuse>=0.5.0,<0.6.0', 'plyer>=1.3.0,<2.0.0', 'requests>=2.19,<3.0']

extras_require = \
{':sys_platform == "linux"': ['dbus-python>=1.2,<2.0']}

entry_points = \
{'console_scripts': ['toasts = toasts.main:main']}

setup_kwargs = {
    'name': 'toasts',
    'version': '0.1.2',
    'description': 'Get desktop notifications from programming websites like GitHub, Stack Overflow and the likes :)',
    'long_description': "# Toasts\n\nToasts is an app that shows desktop notifications from various websites like GitHub,\nStackExchange, BitBucket, and the likes. It just runs in the background and shows\nyou a notification when there is one from sites you have enabled. Authentication to\nyour user account on a particular website is done through a Personal Access Token or\nOauth.\n\n\n*Please do note that this project is still a work in progress, even though it works.*\n\n\n## Supported Sites\n\n- Github\n\nIf you would like a new site to be supported, please open an issue, and let's see\nwhat we can do :)\n\n## Getting Started\n\n### Requirements\n\nToasts is written in Python3 and the package is available on PyPI.\n\nThe app has been tested only on Linux, as of now. It should work fine on a Mac, but\nWindows is not supportd at the moment (I'm working on it).\n\n### Installation\n\nOpen a terminal and:\n\n```shell\n$ pip install --user toasts\n```\n\nFor updating the app:\n```shell\n$ pip install --user -U toasts\n```\n\n### Usage\n\nBefore running the app, we should first enable available clients in the\n[config file](#the-config-file).\nThe user config file is `~/.config/toasts/config.yaml` on Linux and\n`~/Library/Application Support/toasts/config.yaml` on Mac.\n\nOnly Github is implemented for now, so you can enable it in the config file like so:\n\n```yaml\n# Config file for toasts\n\ngeneral:\n        # List of sites to enable; comma seperated list\n        # Default: []\n        clients: [github]\n        .\n        .\n        .\n```\n\nToasts gets Github notifications using a Personal Access Token. Go to\n[Developer Settings](https://github.com/settings/tokens) and create one\nwith permission to access your notifications.\nThen set the environment variables `GH_UNAME` to your Github username and `GH_TOKEN` to the\naccess token you just created (it is possible to authenticate using your Github\npassword; just set `GH_TOKEN` to your password). <!-- security - use password as token -->\n\nYou're all set !\n\nOpen a terminal and and run the `toasts` command:\n\n```shell\n$ toasts\n```\n\nYou should see your notifications pop up, if you have an update from the\nenabled sites.\n\nI'm so happy right now :)\n\n## The Config File\n The file is in [YAML](https://learnxinyminutes.com/docs/yaml/) format:\n\n```yaml\n# Config file for toasts\n\ngeneral:\n        # List of sites to enable; comma seperated list\n        # Default: []\n        clients: []\n        # Connection timeout, in seconds\n        # Default: 7 ; Minimum value: 1\n        conn_timeout: 7\n        # Check for notifications every ___ minutes\n        # Default: 3 ; Minimum value: 2\n        check_every: 3\n        # Show notification for ___ seconds\n        # Default: 7 ; Minimum value: 2\n        notif_timeout: 7\n        # Maximum number of notifications to show at a time, of individual clients.\n        # Default: 2\n        # Note: Value of -1 will show all notifications; it may clutter your workspace.\n        notif_max_show: 2\n\nsites:\n        github:\n                # *Environment variable* which holds your github username\n                # Default: GH_UNAME\n                username: GH_UNAME\n                # *Environment variable* which holds a personal access token for authentication\n                # Default: GH_TOKEN\n                token: GH_TOKEN\n```\n",
    'author': 'Gokul',
    'author_email': 'gokulps15@gmail.com',
    'url': 'https://github.com/gokulsoumya/toasts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
