# HTMLViewer

[![PyPI version shields.io](https://img.shields.io/pypi/v/htmlviewer.svg)](https://pypi.python.org/pypi/htmlviewer/)
[![PyPI license](https://img.shields.io/pypi/l/htmlviewer.svg)](https://pypi.python.org/pypi/htmlviewer/)

Table viewer for relational databases, without using HandsOnTable.

Actually, any list of JSON-serializable dictionaries can be viewed.

This is the remake of [pyhandsontable](https://github.com/patarapolw/pyhandsontable).

## Installation

```
pip install htmlviewer
```

## Usage

In Jupyter Notebook,

```python
>>> from htmlviewer import PagedViewer
>>> viewer = PagedViewer(LIST_OF_RECORDS, **kwargs)
>>> viewer
'A table is shown on Jupyter Notebook.'
>>> viewer.view(-1)
'The last page is shown.'
>>> viewer.previous()
'The previous page (i-1) is shown.'
>>> viewer.next()
'The next page (i+1) is shown.
```

Acceptable kwargs are,

```python
{
    'maxColWidth': 200,  # Maximum column width for all columns.
    'maxRowHeight': 500,  # Maximum row height for all rows.,
    'colWidths': {
        'imageField': 500
    },
    'renderers': {
        'imageField': 'html'  # Set the field to allow HTML.
    }
    'rowHeader': 'id'  # Selecting a custom column to be the first row, aka rowHeader.
}
```

## Embedding images, markdown and HTML.

This can be done in Python side, by converting everything to HTML. Just use [any markdown for Python library](https://github.com/Python-Markdown/markdown).

```python
from markdown import markdown
import base64
image_html = f'<img src="{image_url}" width=100 />'
image_html2 = f'<img src="data:image/png;base64,{base64.b64encode(image_bytes).decode()}" />'
markdown_html = markdown(markdown_raw)
```

Any then,

```python
PagedViewer(LIST_OF_RECORDS, renderers={
    "image_field": "html",
    "html_field": "html",
    "markdown_field": "html"
})
```

## Screenshots

![0.png](/screenshots/0.png)

## Related projects

- [pyhandsontable](https://github.com/patarapolw/pyhandsontable) - View a list of JSON-serializable dictionaries or a 2-D array, in HandsOnTable, in Jupyter Notebook.
