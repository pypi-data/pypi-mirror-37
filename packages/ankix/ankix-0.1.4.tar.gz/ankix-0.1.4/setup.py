# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ankix']

package_data = \
{'': ['*']}

install_requires = \
['datauri',
 'mistune>=0.8.4,<0.9.0',
 'peewee>=3.7,<4.0',
 'pytimeparse>=1.1,<2.0',
 'tqdm>=4.27,<5.0']

setup_kwargs = {
    'name': 'ankix',
    'version': '0.1.4',
    'description': 'New file format for Anki with improved review intervals and Peewee SQLite powered',
    'long_description': "# Ankix\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/ankix.svg)](https://pypi.python.org/pypi/ankix/)\n[![PyPI license](https://img.shields.io/pypi/l/ankix.svg)](https://pypi.python.org/pypi/ankix/)\n\nNew file format for Anki with improved review intervals. Pure [peewee](https://github.com/coleifer/peewee) SQLite database, no zipfile. Available to work with on Jupyter Notebook.\n\n## Usage\n\nOn Jupyter Notebook,\n\n```python\n>>> from ankix import Ankix\n>>> db = Ankix.from_apkg('test.apkg', 'test.ankix')  # A file named 'test.ankix' will be created.\n>>> # Or, db = Ankix('test.ankix')\n>>> iter_quiz = db.iter_quiz()\n>>> card = next(iter_quiz)\n>>> card\n'A flashcard is show on Jupyter Notebook. You can click to change card side, to answer-side.'\n'It is HTML, CSS, Javascript, Image enabled. Cloze test is also enabled. Audio is not yet tested.'\n>>> card.right()  # Mark the card as right\n>>> card.wrong()  # Mark the card as wrong\n>>> card.mark()  # Add the tag 'marked' to the note.\n```\n\nTo view the internal working mechanism, and make use of Peewee capabilities,\n\n```python\n>>> db.tables\n{'tag': <Model: Tag>,\n 'media': <Model: Media>,\n 'model': <Model: Model>,\n 'template': <Model: Template>,\n 'deck': <Model: Deck>,\n 'note': <Model: Note>,\n 'card': <Model: Card>}\n >>> db['card'].select().join(db['note']).where(db['note'].data['field_a'] == 'bar')[0]\n 'The front side of the card is shown.'\n```\n\n## Installation\n\n```commandline\n$ pip install ankix\n```\n\n## Plans\n\n- Test by using it a lot.\n",
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/ankix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
