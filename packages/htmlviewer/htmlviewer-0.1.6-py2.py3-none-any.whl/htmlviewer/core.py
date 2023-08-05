from jinja2 import Environment, PackageLoader
from uuid import uuid4
import os
from threading import Timer
from IPython.display import IFrame

env = Environment(
    loader=PackageLoader('htmlviewer', 'templates')
)


def generate_html(data, **kwargs):
    rowHeader = kwargs.get('rowHeader', None)
    colHeader = []
    for record in data:
        for k in record.keys():
            if k not in colHeader:
                if k == rowHeader:
                    colHeader.insert(0, k)
                else:
                    colHeader.append(k)

    config = {
        'colHeader': colHeader,
        'data': data,
        'maxColWidth': 200,
        'maxRowHeight': 500,
    }
    config.update(kwargs)

    template = env.get_template('viewer.html')
    return template.render(config=config)


def view_table(data, width=1000, height=500,
               filename=None, autodelete=True, **kwargs):
    # A TemporaryFile does not work with Jupyter Notebook

    if filename is None:
        filename = str(uuid4()) + '.html'

    try:
        with open(filename, 'w') as f:
            f.write(generate_html(data=data, width=width, height=height, **kwargs))

        return IFrame(filename, width=width, height=height)
    finally:
        if autodelete:
            Timer(5, os.unlink, args=[filename]).start()
