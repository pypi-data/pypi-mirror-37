# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['astdiff']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.7,<7.0',
 'colorful>=0.4.1,<0.5.0',
 'six>=1.11,<2.0',
 'typing>=3.6,<4.0']

entry_points = \
{'console_scripts': ['astdiff = astdiff:astdiff.astdiff']}

setup_kwargs = {
    'name': 'astdiff',
    'version': '0.2.1',
    'description': 'Ensure the invariance of the Abstract Syntax Tree across commits.',
    'long_description': '# ASTdiff\n\nCompare two commits in a git repository to guarantee that there are no semantic changes.\n\nUse this tool to corroborate that formatting tools don\'t change the code. If `astdiff` returns 0, the Abstract Syntax \nTree of the files changed in the commits is the same.\n\n\n## Installation\n\nUsing `pip`:\n\n```shell\npip install astdiff\n```\n\n\n### Development Installation\n\nTo audit the code, or to modify it, install `astdiff` in development mode. The tool uses [poetry](https://poetry.eustace.io/) to manage dependencies\nand to build `pip` installable packages. \n\n```bash\n$ git clone https://github.com/auntbertha/astdiff.git\n$ cd astdiff\n$ poetry develop\n$ poetry run pytest\n```\n\nTo build new packages:\n\n```bash\n$ poetry build\n```\n\nand distribute the wheel or tarball from the directory `dist/`.\n\n\n## Usage\n\nThe most basic use of `astdiff` is to check that a reformatting tool didn\'t change the meaning of the code. When it\'s\ncalled with no arguments `astdiff` compares the working tree against the HEAD of the current branch:\n\n```bash\n$ astdiff\nRunning: git diff --name-only 9d3219ba027d5a56040d23eb9ee3d23f7a410ad5\nChecking astdiff/astdiff.py ... ok\n✨ All files are equivalent! ✨\n$ echo $?\n0\n```\n\n`astdiff` returns 0 if the ASTs are the same, and returns 1 otherwise. The messages are printed to standard error.\n\n`astdiff` can also check a given commit, a given commit and the working tree, or any pair of commits. It accepts the\nnames of the commits in the same way that `git` does.\n\nUse `-h` or `--help` to get help:\n\n```bash\n$ astdiff -h\nUsage: astdiff.py [OPTIONS] [COMMITS]...\n\n  Compare the AST of all changed files between commits.\n\n  With no arguments, compare between HEAD and the working tree.\n  With one argument COMMIT, compare between COMMIT~1 and COMMIT.\n  With two arguments, COMMIT1 and COMMIT2, compare between those two.\n\n  (COMMIT2 can be a dot \'.\' to compare between COMMIT1 and the working tree)\n\nOptions:\n  -h, --help  Show this message and exit.\n```\n\n\n## Algorithm\n\nThe comparison of the ASTs is a very simple recursive function that traverses the trees in a pre-order depth-first \nsearch. It can be audited to verify its correctness: `astdiff.compare_ast`.\n\n\n## LICENSE\n\n### The MIT License (MIT)\n\nCopyright © 2018 Aunt Bertha\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.',
    'author': 'Walter Moreira',
    'author_email': 'wmoreira@auntbertha.com',
    'url': 'https://github.com/auntbertha/ASTdiff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
