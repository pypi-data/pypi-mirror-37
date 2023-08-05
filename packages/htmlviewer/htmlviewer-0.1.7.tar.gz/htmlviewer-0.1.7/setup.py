# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['htmlviewer']

package_data = \
{'': ['*'], 'htmlviewer': ['templates/*']}

install_requires = \
['jinja2>=2.10,<3.0', 'jupyter>=1.0,<2.0', 'notebook>=5.7,<6.0']

setup_kwargs = {
    'name': 'htmlviewer',
    'version': '0.1.7',
    'description': 'Table viewer for relational databases, without using HandsOnTable.',
    'long_description': '# HTMLViewer\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/htmlviewer.svg)](https://pypi.python.org/pypi/htmlviewer/)\n[![PyPI license](https://img.shields.io/pypi/l/htmlviewer.svg)](https://pypi.python.org/pypi/htmlviewer/)\n\nTable viewer for relational databases, without using HandsOnTable.\n\nActually, any list of JSON-serializable dictionaries can be viewed.\n\nThis is the remake of [pyhandsontable](https://github.com/patarapolw/pyhandsontable).\n\n## Installation\n\n```\npip install htmlviewer\n```\n\n## Usage\n\nIn Jupyter Notebook,\n\n```python\n>>> from htmlviewer import PagedViewer\n>>> viewer = PagedViewer(LIST_OF_RECORDS, **kwargs)\n>>> viewer\n\'A table is shown on Jupyter Notebook.\'\n>>> viewer.view(-1)\n\'The last page is shown.\'\n>>> viewer.previous()\n\'The previous page (i-1) is shown.\'\n>>> viewer.next()\n\'The next page (i+1) is shown.\n```\n\nAcceptable kwargs are,\n\n```python\n{\n    \'maxColWidth\': 200,  # Maximum column width for all columns.\n    \'minColWidth\': \'8em\',\n    \'maxRowHeight\': 500,  # Maximum row height for all rows.,\n    \'colWidth\': {\n        \'imageField\': 500\n    },\n    \'renderer\': {\n        \'imageField\': \'html\'  # Set the field to allow HTML.\n    }\n    \'rowHeader\': \'id\'  # Selecting a custom column to be the first row, aka rowHeader.\n}\n```\n\n## Embedding images, markdown and HTML.\n\nThis can be done in Python side, by converting everything to HTML. Just use [any markdown for Python library](https://github.com/Python-Markdown/markdown).\n\n```python\nfrom markdown import markdown\nimport base64\nimage_html = f\'<img src="{image_url}" width=100 />\'\nimage_html2 = f\'<img src="data:image/png;base64,{base64.b64encode(image_bytes).decode()}" />\'\nmarkdown_html = markdown(markdown_raw)\n```\n\nAny then,\n\n```python\nPagedViewer(LIST_OF_RECORDS, renderers={\n    "image_field": "html",\n    "html_field": "html",\n    "markdown_field": "html"\n})\n```\n\n## Screenshots\n\n![0.png](/screenshots/0.png)\n\n## Related projects\n\n- [pyhandsontable](https://github.com/patarapolw/pyhandsontable) - View a list of JSON-serializable dictionaries or a 2-D array, in HandsOnTable, in Jupyter Notebook.\n',
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/htmlviewer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
