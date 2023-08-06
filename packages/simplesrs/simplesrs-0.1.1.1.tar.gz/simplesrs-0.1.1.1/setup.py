# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['simplesrs']

package_data = \
{'': ['*']}

install_requires = \
['peewee>=3.7,<4.0']

setup_kwargs = {
    'name': 'simplesrs',
    'version': '0.1.1.1',
    'description': 'Simple SRS (spaced-recognition system) mechanism and database',
    'long_description': "# simplesrs\n\nSimple SRS (spaced-recognition system) mechanism and database. Scalable and zero configuration.\n\n## Usage\n\n```python\n>>> import simplesrs as srs\n>>> srs.init('srs.db')\n>>> srs.Card.add('类', tags=['hanzi', 't_hanzi1'], vocabs=['人类 人類 [ren2 lei4] humanity/human race/mankind'])\n>>> srs.Card.add('数学', tags=['vocab', 'pleco'])\n>>> srs.Card.add('重要的事情要立即去做', tags=['sentence', 't_hanzi1'], translation='重要的事情要立即去做。 [Zhòngyào de shìqing yào lìjí qù zuò. (Also no qu (less strong))] I need to go do important things immediately.')\n>>> quiz = srs.Card.iter_quiz()\n>>> card = next(quiz)\n>>> card\n重要的事情要立即去做\n>>> card.info\n{\n    'translation':\n        '重要的事情要立即去做。 [Zhòngyào de shìqing yào lìjí qù zuò. (Also no qu (less '\n        'strong))] I need to go do important things immediately.'\n}\n>>> card.right()  # Mark as right, and next review by now() + srs_level's timedelta()\n>>> card.undo()  # Undo marking as right.\n>>> card.wrong()  # Mark as wrong, and bury for default: 10 minutes.\n>>> card.undo()\n>>> card.bury()  # Bury for default: 4 hours\n```\n\n## Installation\n\n```\npip install simplesrs\n```\n\n## Related projects\n\n- [ankix](https://github.com/patarapolw/ankix) -- New file format for Anki with improved review intervals. Pure peewee SQLite database, no zipfile, but media enabled. Available to work with on Jupyter Notebook. Full dropin replacement for Anki. \n",
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/simplesrs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
