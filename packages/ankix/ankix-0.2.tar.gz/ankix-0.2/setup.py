# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ankix']

package_data = \
{'': ['*']}

install_requires = \
['mistune>=0.8.4,<0.9.0',
 'peewee>=3.7,<4.0',
 'python-magic>=0.4.15,<0.5.0',
 'pytimeparse>=1.1,<2.0',
 'tqdm>=4.27,<5.0']

setup_kwargs = {
    'name': 'ankix',
    'version': '0.2',
    'description': 'New file format for Anki with improved review intervals and Peewee SQLite powered',
    'long_description': "# Ankix\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/ankix.svg)](https://pypi.python.org/pypi/ankix/)\n[![PyPI license](https://img.shields.io/pypi/l/ankix.svg)](https://pypi.python.org/pypi/ankix/)\n\nNew file format for Anki with improved review intervals. Pure [peewee](https://github.com/coleifer/peewee) SQLite database, no zipfile. Available to work with on Jupyter Notebook.\n\n## Usage\n\nOn Jupyter Notebook,\n\n```python\n>>> from ankix import ankix, db as a\n>>> ankix.init('test.ankix')  # A file named 'test.ankix' will be created.\n>>> ankix.import_apkg('foo.apkg')  # Import the contents from 'foo.apkg'\n>>> iter_quiz = a.iter_quiz()\n>>> card = next(iter_quiz)\n>>> card\n'A flashcard is show on Jupyter Notebook. You can click to change card side, to answer-side.'\n'It is HTML, CSS, Javascript, Image enabled. Cloze test is also enabled. Audio is not yet tested.'\n>>> card.right()  # Mark the card as right\n>>> card.wrong()  # Mark the card as wrong\n>>> card.mark()  # Add the tag 'marked' to the note.\n```\n\nYou can directly make use of Peewee capabilities,\n\n```python\n >>> a.Card.select().join(a.Note).where(a.Note.data['field_a'] == 'bar')[0]\n 'The front side of the card is shown.'\n```\n\n## Adding new cards\n\nAdding new cards is now possible. This has been tested in https://github.com/patarapolw/zhlib/blob/master/zhlib/export.py#L15\n\n```python\nfrom ankix import ankix, db as a\nankix.init('test.ankix')\na_model = a.Model.add(\n    name='foo',\n    templates=[\n        a.TemplateMaker(\n            name='Forward', \n            question=Q_FORMAT,\n            answer=A_FORMAT\n        ),\n        a.TemplateMaker(\n            name='Reverse', \n            question=Q_FORMAT,\n            answer=A_FORMAT)\n    ],\n    css=CSS,\n    js=JS\n)\n# Or, a_model = a.Model.get(name='foo')\nfor record in records:\n    a.Note.add(\n        data=record,\n        model=a_model,\n        card_to_decks={\n            'Forward': 'Forward deck',\n            'Reverse': 'Reverse deck'\n        },\n        tags=['bar', 'baz']\n    )\n```\n\n## Installation\n\n```commandline\n$ pip install ankix\n```\n\n## Plans\n\n- Test by using it a lot.\n",
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/ankix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
