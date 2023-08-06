jupyter-extjs
===============================

An ExtJS Jupyter extension

Installation
------------
To build and deploy:

    $ python setup.py sdist upload

To install use pip:

    $ pip install extjs
    $ jupyter nbextension enable --py --sys-prefix extjs

For a development installation (requires npm),

    $ git clone https://github.com/MPetrashev/jupyter-extjs.git
    $ cd jupyter-extjs
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix extjs
    $ jupyter nbextension enable --py --sys-prefix extjs
