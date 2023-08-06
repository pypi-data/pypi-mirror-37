# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dotedit']

package_data = \
{'': ['*'],
 'dotedit': ['completions/bash/*', 'completions/fish/*', 'completions/zsh/*']}

entry_points = \
{'console_scripts': ['dotedit = dotedit.__main__:main']}

setup_kwargs = {
    'name': 'dotedit',
    'version': '1.2.0',
    'description': 'Edit dotfiles easily',
    'long_description': '# dotedit\nOpens the configuration file (dotfile) for a given program. \n\n#### Contents\n1. [Usage](#usage)\n   * [Hooks](#hooks)\n2. [Install](#install)\n    * [Bash](#bash)\n    * [Zsh](#zsh)\n    * [fish](#fish)\n\n## Usage\n\nOpen configuration file for conky:\n\n```bash\n$ dotedit c<TAB>        # <-- Tab-completion for bash, zsh & fish!\n$ dotedit conky\n# opens ~/.config/conky/conky.conf in $EDITOR\n```\n\nIf dotedit does not know the path to the dotfile for a program, it will try to find it in `$XDG_CONFIG_HOME` or `$HOME`. It will always prompt before adding a path to avoid opening the wrong file:\n\n```bash\n$ dotedit bspwm\nAdd path to bspwm: ~/.config/bspwm/bspwmrc        # <-- Tab-completion works here too!\n#opens ~/.config/bspwm/bspwmrc in $EDITOR\n```\n\ndotedit will, of course, save the path for next time:\n\n```bash\n$ dotedit bspwm\n#opens ~/.config/bspwm/bspwmrc in $EDITOR\n```\n\nIf you mistype...\n\n```bash\n$ dotedit xinit\nAdd path to xinit: ~/.xinitcr        # <-- Doh!\n```\n\n...you can update the path...\n\n```bash\n$ dotedit --update xinit\nUpdate path to xinit: ~/.xinitcr\nUpdate path to xinit: ~/.xinit\nUpdate path to xinit: ~/.xinitrc\n```\n\n...or just remove it:\n\n```bash\n$ dotedit --remove xinit\n```\n\n### Hooks\nYou can add pre and post hooks by creating the files\n`$XDG_CONFIG_HOME/dotedit/hooks/pre-edit` and \n`$XDG_CONFIG_HOME/dotedit/hooks/postedit` and making them executable.\n\nFor example to automatically commit and push changes to dotfiles in a git\ndirectory you can create post edit hook with the following content:\n\n```bash\n#!/bin/sh\n\ncd "$HOME/git/dotfiles/" | return\ngit add -A . && git commit -m \'update\' && git pull --rebase && git push\n```\n\n## Install\n\n```bash\n$ pip3 install --user dotedit\n```\n\n### Completions\nTo enable completions, the completion scripts need to be installed manually. \n\n#### Bash\n```bash\n$ dotedit --completions bash > ~/.local/share/bash-completion/completions/dotedit\n```\n\n#### Zsh\n\n```zsh\n$ dotedit --completions zsh > ~/.zfunc/_dotedit\n```\n\n#### fish\n\n```fish\n$ dotedit --completions fish > ~/.config/fish/completions/dotedit.fish\n```\n\nFinally, restart your shell session or source the completion script to enable completions.\n',
    'author': 'Daniel Alm Grundström',
    'author_email': 'daniel.alm.grundstrom@protonmail.com',
    'url': 'https://github.com/almgru/dotedit',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
