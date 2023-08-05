# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pdf_shuffle']

package_data = \
{'': ['*'], 'pdf_shuffle': ['static/*', 'templates/*']}

install_requires = \
['click>=7.0,<8.0', 'flask>=1.0,<2.0']

entry_points = \
{'console_scripts': ['pdf-quiz = pdf_shuffle.__main__:pdf_quiz',
                     'pdf-shuffle = pdf_shuffle.__main__:pdf_shuffle']}

setup_kwargs = {
    'name': 'pdf-shuffle',
    'version': '0.2.1',
    'description': 'A PDF page/image randomizer, or flashcard quiz from a PDF.',
    'long_description': "# pdf-shuffle\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/pdf_shuffle.svg)](https://pypi.python.org/pypi/pdf_shuffle/)\n[![PyPI license](https://img.shields.io/pypi/l/pdf_shuffle.svg)](https://pypi.python.org/pypi/pdf_shuffle/)\n\nA PDF page/image randomizer, or flashcard quiz from a PDF. Or randomize files from a folder.\n\n## Installation\n\n```\n$ pip install pdf-shuffle\n```\n\n## Usage\n\npdf-shuffle comes with 2 CLI applications:\n\n```\n$ pdf-shuffle --help\nUsage: pdf-shuffle [OPTIONS] FILENAME\n\nOptions:\n  --start INTEGER\n  --end TEXT\n  --step INTEGER\n  --random / --no-random\n  --host TEXT\n  --port INTEGER\n  --help                  Show this message and exit.\n$ pdf-shuffle test.pdf\n```\n\nAnd,\n\n```\n$ pdf-quiz --help\nUsage: pdf-quiz [OPTIONS] FILENAME\n\nOptions:\n  --start INTEGER\n  --end TEXT\n  --step INTEGER\n  --random / --no-random\n  --host TEXT\n  --port INTEGER\n  --help                  Show this message and exit.\n$ pdf-quiz quiz.pdf\n```\n\nOf course, you can invoke the app from a Python script as well.\n\n```python\nfrom pdf_shuffle import init\ninit('test.pdf')\n```\n\nOr,\n\n```python\nfrom pdf_shuffle import init_quiz\ninit_quiz('quiz.pdf')\n```\n\nYou can also random files in a folder:\n\n```python\nfrom pdf_shuffle import init\ninit('test/')\n```\n\n## Advanced usage\n\nBy default, `quiz.pdf` means, excluding the first slide, every first and second slides are front of the card and back of the card, respectively. You can change that, with:\n\n```python\nimport os, json\nos.environ['PAGE_RANDOM'] = json.dumps([2, 3, 5, 9, 12])\n```\n\n## Spaced-repetition system (SRS)\n\nIf you are looking into extending the app with SRS, you might try, [srs-sqlite](https://github.com/patarapolw/srs-sqlite), which I currently use.\n",
    'author': 'patarapolw',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/pdf-shuffle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
