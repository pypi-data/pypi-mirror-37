# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['imserv']

package_data = \
{'': ['*'], 'imserv': ['static/*', 'templates/*']}

install_requires = \
['click>=7.0,<8.0',
 'flask>=1.0,<2.0',
 'imagehash>=4.0,<5.0',
 'nonrepeat>=0.1.1,<0.2.0',
 'peewee>=3.7,<4.0',
 'pillow>=5.2,<6.0',
 'psycopg2-binary>=2.7,<3.0',
 'python-slugify>=1.2,<2.0',
 'send2trash',
 'tqdm>=4.26,<5.0',
 'watchdog>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['imserv = imserv.__main__:runserver']}

setup_kwargs = {
    'name': 'imserv',
    'version': '0.1.11.4',
    'description': 'Spin an image server, store images from Clipboard in single place, and prevent duplication.',
    'long_description': "# ImServ\n\nSpin an image server, store images from Clipboard in single place, and prevent duplication.\n\n## Installation\n\n- Clone the project from GitHub\n- Navigate to the project folder and [`poetry install`](https://github.com/sdispater/poetry)\n- Run a Python script:\n\n```python\nfrom imserv.db import create_all_tables\ncreate_all_tables()\n```\nThe folder `~/Pictures/imserv` will be created, and will be used for storing all images. (Tested only on Mac.)\n\nBy default, it uses PostGRESQL of the database named `imserv`, so you have to initialize the database first, before running the script.\n\nThe image folder can also be changed in `ImServ(folder=IMG_FOLDER_PATH)`.\n\n## Usage\n\nTo run an image server (before running Jupyter Notebook), run in a script:\n\n```python\nImServ().runserver()\n```\n\nThis will open the server for the website: http://localhost:8000/, which leads to:\n\n![web.png](/screenshots/web.png)\n\nwhere you can create an image directly from Clipboard. The name of the image will be randomized using UUID.\n\nAfter that, if you want to use it in Jupyter Notebook:\n\n```python\n>>> from imserv import ImServ\n>>> ims = ImServ()\n>>> ims.last()\n'The image accessed last will be shown.'\n```\n\n## More screenshots\n\n![jupyter0.png](/screenshots/jupyter0.png)\n![jupyter1.png](/screenshots/jupyter1.png)\n\n## Related projects\n\n- [jupyter-flashcard](https://github.com/patarapolw/jupyter-flashcard) - Create a database of Jupyter Notebooks and convert them into flashcards.\n",
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/imserv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
