# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['edfrd']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.15,<2.0']

setup_kwargs = {
    'name': 'edfrd',
    'version': '0.1',
    'description': 'edfrd is a Python 3 software library to read EDF files.',
    'long_description': "# edfrd\n\nedfrd is a Python 3 software library to read EDF files.\n\n## Installation\n\n```bash\npip3 install --user edfrd\n```\n\n## Usage\n\n```python\nfrom edfrd import read_edf, read_signal\n\nfile_path = 'PATH/TO/FILE.edf'\n\nedf = read_edf(file_path)\n\nsignals = [\n    read_signal(file_path, edf, i)\n    for i in range(edf.number_of_signals)\n]\n```\n",
    'author': 'Christoph Jansen',
    'author_email': 'Christoph.Jansen@htw-berlin.de',
    'url': 'https://cbmi.htw-berlin.de/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
