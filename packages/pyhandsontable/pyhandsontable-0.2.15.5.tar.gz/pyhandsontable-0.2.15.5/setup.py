# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyhandsontable']

package_data = \
{'': ['*'], 'pyhandsontable': ['templates/*']}

install_requires = \
['jinja2>=2.10,<3.0', 'jupyter>=1.0,<2.0', 'notebook>=5.6,<6.0']

setup_kwargs = {
    'name': 'pyhandsontable',
    'version': '0.2.15.5',
    'description': 'View a list of dictionaries or a 2-D array, in HandsOnTable, in Jupyter Notebook.',
    'long_description': '# pyhandsontable\n\n[![Build Status](https://travis-ci.org/patarapolw/pyhandsontable.svg?branch=master)](https://travis-ci.org/patarapolw/pyhandsontable)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/pyhandsontable.svg)](https://pypi.python.org/pypi/pyhandsontable/)\n[![PyPI license](https://img.shields.io/pypi/l/pyhandsontable.svg)](https://pypi.python.org/pypi/pyhandsontable/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pyhandsontable.svg)](https://pypi.python.org/pypi/pyhandsontable/)\n\nView a list of JSON-serializable dictionaries or a 2-D array, in HandsOnTable, in Jupyter Notebook.\n\nNested JSON renderer is also supported and is default. Image and markdown renderers are possible, but has to be extended.\n\n## Installation\n\n```commandline\npip install pyhandsontable\n```\n\n## Usage\n\nIn Jupyter Notebook,\n\n```python\n>>> from pyhandsontable import PagedViewer\n>>> viewer = PagedViewer(data=data_matrix, **kwargs)\n>>> viewer\n\'A Handsontable is shown in Jupyter Notebook.\'\n>>> viewer.view(-1)\n\'The last page is shown.\'\n>>> viewer.previous()\n\'The previous page (i-1) is shown.\'\n>>> viewer.next()\n\'The next page (i+1) is shown.\'\n```\n\nData matrix can be either a list of lists (2-D array) or a list of dictionaries.\n\nIt is also possible to view all entries at once, but it could be bad, if there are too many rows.\n\n```python\n>>> from pyhandsontable import view_table\n>>> view_table(data_matrix, **kwargs)\n```\n\n## Acceptable kwargs\n\n- height: height of the window (default: 500)\n- width: width of the window (default: 1000)\n- title: title of the HTML file\n- maxColWidth: maximum column width. (Default: 200)\n- renderers: the renderers to use in generating the columns (see below.)\n- autodelete: whether the temporary HTML file should be autodeleted. (Default: True)\n- filename: filename of the temporary HTML file (default: \'temp.handsontable.html\')\n- config: add additional config as defined in https://docs.handsontable.com/pro/5.0.0/tutorial-introduction.html\n  - This will override the default config (per key basis) which are:\n  \n```javascript\n{\n    data: data,\n    rowHeaders: true,\n    colHeaders: true,\n    columns: columns,\n    manualColumnResize: true,\n    manualRowResize: true,\n    renderAllRows: true,\n    modifyColWidth: (width, col)=>{\n        if(width > maxColWidth) return maxColWidth;\n    },\n    afterRenderer: (td, row, column, prop, value, cellProperties)=>{\n        td.innerHTML = \'<div class="wrapper"><div class="wrapped">\' + td.innerHTML + \'</div></div>\';\n    }\n}\n```\n\n`renderers` example, if your data is a 2-D array:\n\n```python\n{\n    1: \'html\',\n    2: \'html\'\n}\n```\n\nor if your data is list of dict:\n\n```python\n{\n    "front": \'html\',\n    "back": \'html\'\n}\n```\n\n## Enabling Image, HTML and Markdown renderer\n\nThis can be done in Python side, by converting everything to HTML. Just use [any markdown for Python library](https://github.com/Python-Markdown/markdown).\n\n```python\nfrom markdown import markdown\nimport base64\nimage_html = f\'<img src="{image_url}" width=100 />\'\nimage_html2 = f\'<img src="data:image/png;base64,{base64.b64encode(image_bytes).decode()}" />\'\nmarkdown_html = markdown(markdown_raw)\n```\n\nAny then,\n\n```python\nPagedViewer(data=data_matrix, renderers={\n    "image_field": "html",\n    "html_field": "html",\n    "markdown_field": "html"\n})\n```\n\n## Screenshots\n\n![1.png](/screenshots/1.png?raw=true)\n![0.png](/screenshots/0.png?raw=true)\n\n## Related projects\n\n- [htmlviewer](https://github.com/patarapolw/htmlviewer) - similar in concept to this project, but does not use HandsOnTable.js\n- [TinyDB-viewer](https://github.com/patarapolw/tinydb-viewer) - uses HandsOnTable.js and also allow editing in Jupyter Notebook. \n\n## License\n\nThis software includes [`handsontable.js`](https://github.com/handsontable/handsontable), which is MIT-licensed.\n',
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/pyhandsontable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
