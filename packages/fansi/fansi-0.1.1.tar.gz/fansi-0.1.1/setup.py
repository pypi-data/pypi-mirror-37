# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fansi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fansi',
    'version': '0.1.1',
    'description': 'A Python library that makes formatting, colouring and adding emojis to terminal printouts easy.',
    'long_description': '# Fansi\nFansi is a Python library that makes formatting, colouring and adding emojis to terminal printouts easy.\n\n# Installation\n\n`pip install fansi`\n\nTo uninstall: `pip uninstall fansi`\n\n# Usage\n## First steps\nFirst, include fansi in your script: \n\n> `from fansi import fansi`\n\nThen, instead of `print()` statements, use `fansi.say()`\n\n> `fansi.say("This string can have fansi formatting!")`\n\n## Basic formatting\n\nTo add italics, use `_tags_` or `*tags*`. To add bolding, use `__tags__` or `**tags**`. To add bolding and italics, use `___tags___` or `***tags***`.\n\nFor example:\n> `fansi.say("This _text will be italicised. __This text will be **bolded**. ___This text will be both___")`\n\n## Inline tagging\n\nYou can add Ansi formatting characters inline, affecting the colour or emphasis of your text, using `::tags::` To reset the formatting, use the `::end::` tag.\n\nFor example: \n> `fansi.say("This text will be normal. ::green bold italics:: This text will be green, bold and italicised. ::end:: This text will be back to normal.")`\n\n## Global tags\n\nFansi tags can also be added to the entire string.\n\nFor example: `fansi.say("This text will be magenta on a green background.", "magenta bg-green")`\n\n## Emojis\n\nYou can also add any emoji, using `:tags:`. Long and shortnames work.\n\nFor example: \n> `fansi.say("Here are some :poop: emojis! :panda_face::tiger:cat:")`\'\n\nThat\'s it!\n',
    'author': 'Daniel Rivas Perez',
    'author_email': 'drivas12@googlemail.com',
    'url': 'https://github.com/drivasperez/fansi/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
