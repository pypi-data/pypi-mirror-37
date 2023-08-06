# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fansi']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'fansi',
    'version': '0.1.4',
    'description': 'A Python library that makes formatting, colouring and adding emojis to terminal printouts easy.',
    'long_description': '# Fansi\nFansi is a Python library that makes formatting, colouring and adding emojis to terminal printouts easy.\n\n![fansi demo](https://i.postimg.cc/zGcL6MhG/Screenshot-2018-10-26-at-13-40-19.png)\n\n# Installation\n\n`pip install fansi`\n\nTo uninstall: `pip uninstall fansi`\n\n# Usage\n## First steps\nFirst, include fansi in your script: \n\n> `from fansi import fansi`\n\nThen, instead of `print()` statements, use `fansi.say()`.\n\n> `fansi.say("This string can have fansi formatting!")`\n\nIf you want to generate a formatted string without printing it, use `fansi.format()`.\n\n> `a = fansi.format("Here\'s a string ::blue:: formatted with Ansi characters! ::end:: It\'s partly blue!")`\n\n## Basic formatting\n\nTo add italics, use `_tags_` or `*tags*`. To add bolding, use `__tags__` or `**tags**`. To add bolding and italics, use `___tags___` or `***tags***`.\n\nFor example:\n> `fansi.say("This _text will be italicised_. This text will be **bolded**. ___This text will be both___.")`\n\n## Inline tagging\n\nYou can add Ansi formatting characters inline, affecting the colour or emphasis of your text, using `::tags::` To reset the formatting, use the `::end::` tag.\n\nFor example: \n> `fansi.say("This text will be normal. ::green bold italics:: This text will be green, bold and italicised. ::end:: This text will be back to normal.")`\n\n## Global tags\n\nFansi tags can also be added to the entire string.\n\nFor example: `fansi.say("This text will be magenta on a blue background.", "magenta bg-blue")`\n\n## Emojis\n\nYou can also add any emoji, using `:tags:`. Long and shortnames work.\n\nFor example: \n> `fansi.say("Here are some :poop: emojis! :panda_face::tiger::cat:")`\'\n\nThat\'s it!\n\n# Appendix: Fansi tags\n\n| Tag          | Description           |\n|--------------|-----------------------|\n| `bold`       | Bold text             |\n| `italics`    | Italicised text       |\n| `underline`  | Underlined text       |\n| `blink`      | Blinking text (don\'t) |\n| `invisible`  | Invisible text        |\n|--------------|-----------------------|\n| `black`      | Black text            |\n| `red`        | Red text              |\n| `green`      | Green text            |\n| `yellow`     | Yellow text           |\n| `blue`       | Blue text             |\n| `magenta`    | Magenta text          |\n| `cyan`       | Cyan text             |\n| `white`      | White text            |\n|--------------|-----------------------|\n| `bg-black`   | Black background      |\n| `bg-red`     | Red background        |\n| `bg-green`   | Green background      |\n| `bg-yellow`  | Yellow background     |\n| `bg-blue`    | Blue background       |\n| `bg-magenta` | Magenta background    |\n| `bg-cyan`    | Cyan background       |\n| `bg-white`   | White background      |\n',
    'author': 'Daniel Rivas Perez',
    'author_email': 'drivas12@googlemail.com',
    'url': 'https://github.com/drivasperez/fansi/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
