# pull-repos

[![PyPI](https://img.shields.io/pypi/v/pull-repos.svg)](https://pypi.org/project/pull-repos/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pull-repos.svg)
[![PyPI - License](https://img.shields.io/pypi/l/pull-repos.svg)](./LICENSE)

pull-repos clones and updates repositories in a specific directory

### Requirements

git must be installed in your OS

### Installation

    pip install pull-repos

### Usage

For all sections in config file

    pull-repos ./config.ini

or

    pull-repos ./config.ini:default

for one specified section

Example of _config.ini_:

    [default]
    dir=/home/data/projects/myprojects
    repos=
        git@github.com:pikhovkin/null_object.git
    
    [github]
    dir=/home/data/projects/github/
    repos=
        git@github.com:pikhovkin/yametrikapy.git
        git@github.com:pikhovkin/null_object.git

### License

MIT
