# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cotinga',
 'cotinga.core',
 'cotinga.core.pmdoc',
 'cotinga.gui',
 'cotinga.gui.core',
 'cotinga.gui.dialogs',
 'cotinga.gui.panels',
 'cotinga.gui.pupils_progression_manager',
 'cotinga.gui.pupils_progression_manager.dialogs',
 'cotinga.gui.pupils_progression_manager.dialogs.pages',
 'cotinga.models']

package_data = \
{'': ['*'],
 'cotinga': ['data/*',
             'data/default/*',
             'data/default/data/*',
             'data/default/data/pmdoc/*',
             'data/default/data/prefs/*',
             'data/default/files/*',
             'data/default/files/pmdocsettings/*',
             'data/locale/*',
             'data/locale/en_US/*',
             'data/locale/en_US/LC_MESSAGES/*',
             'data/locale/fr_FR/*',
             'data/locale/fr_FR/LC_MESSAGES/*',
             'data/pics/*',
             'data/pics/flags/*',
             'data/run/*',
             'data/run/pmdoc/*']}

install_requires = \
['Babel>=2.6,<3.0',
 'file-magic>=0.4.0,<0.5.0',
 'mathmakerlib>=0.7.0,<0.8.0',
 'pygobject>=3.28,<4.0',
 'reportlab>=3.5,<4.0',
 'sqlalchemy-utils>=0.33.3,<0.34.0',
 'sqlalchemy>=1.2,<2.0',
 'toml>=0.9.4,<0.10.0']

entry_points = \
{'console_scripts': ['cotinga = cotinga.gui:run']}

setup_kwargs = {
    'name': 'cotinga',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Nicolas Hainaux',
    'author_email': 'nh.techn@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
