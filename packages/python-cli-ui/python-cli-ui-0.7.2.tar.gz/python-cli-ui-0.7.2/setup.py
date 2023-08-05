# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ui', 'ui.tests']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.3,<0.4', 'tabulate>=0.8,<0.9', 'unidecode>=1.0,<2.0']

setup_kwargs = {
    'name': 'python-cli-ui',
    'version': '0.7.2',
    'description': 'Build Nice User Interfaces In The Terminal',
    'long_description': 'python-cli-ui\n=============\n\nTools for nice user interfaces in the terminal.\n\n.. image:: https://img.shields.io/travis/SuperTanker/python-cli-ui.svg?branch=master\n  :target: https://travis-ci.org/SuperTanker/python-cli-ui\n\n.. image:: https://img.shields.io/pypi/v/python-cli-ui.svg\n  :target: https://pypi.org/project/python-cli-ui/\n\n.. image:: https://img.shields.io/github/license/SuperTanker/python-cli-ui.svg\n  :target: https://github.com/SuperTanker/python-cli-ui/blob/master/LICENSE\n\n\nDocumentation\n-------------\n\n\nSee `python-cli-ui documentation <https://supertanker.github.io/python-cli-ui>`_.\n\nDemo\n----\n\n\nWatch the `asciinema recording <https://asciinema.org/a/112368>`_.\n\n\nUsage\n-----\n\n.. code-block:: console\n\n    $ pip install python-cli-ui\n\nExample:\n\n.. code-block:: python\n\n    import ui\n\n    # coloring:\n    ui.info("This is", ui.red, "red",\n            ui.reset, "and this is", ui.bold, "bold")\n\n    # enumerating:\n    list_of_things = ["foo", "bar", "baz"]\n    for i, thing in enumerate(list_of_things):\n        ui.info_count(i, len(list_of_things), thing)\n\n    # progress indication:\n    ui.info_progress("Done",  5, 20)\n    ui.info_progress("Done", 10, 20)\n    ui.info_progress("Done", 20, 20)\n\n    # reading user input:\n    with_sugar = ui.ask_yes_no("With sugar?", default=False)\n\n    fruits = ["apple", "orange", "banana"]\n    selected_fruit = ui.ask_choice("Choose a fruit", fruits)\n\n    #  ... and more!\n',
    'author': 'Dimitir Merejkowsky',
    'author_email': None,
    'url': 'https://github.com/SuperTanker/python-cli-ui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
