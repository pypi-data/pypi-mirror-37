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
    'version': '0.3',
    'description': 'edfrd is a Python 3 software library to read EDF files.',
    'long_description': "# edfrd\n\nedfrd is a Python 3 software library to read EDF files.\n\n## Installation\n\n```bash\npip3 install --user edfrd\n```\n\n## Usage\n\n```python\nfrom edfrd import read_edf, read_data_records\n\nfile_path = 'PATH/TO/FILE.edf'\n\nedf = read_edf(file_path)  # namedtuple\n\ndata_records = [\n    data_record for data_record in\n    read_data_records(file_path, edf)  # generator\n]\n\nassert len(data_records[0]) == edf.number_of_signals\n```\n",
    'author': 'Christoph Jansen',
    'author_email': 'Christoph.Jansen@htw-berlin.de',
    'url': 'https://cbmi.htw-berlin.de/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
