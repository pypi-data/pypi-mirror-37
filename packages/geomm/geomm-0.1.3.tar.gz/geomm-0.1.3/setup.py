# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['geomm']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.28.5,<0.29.0', 'numpy>=1.15,<2.0', 'scipy>=1.1,<2.0']

setup_kwargs = {
    'name': 'geomm',
    'version': '0.1.3',
    'description': 'Simple and stupid library for strictly geometric (geom) operations (zero-knowledge of topology) common to computational biology and chemistry macromolecules (mm).',
    'long_description': '* GEOMM\n\nA simple no-nonsense library for computing common geometry on\nmacromolecular systems.\n\nThis library aims to work completely on numpy arrays and knows nothing\nabout molecule or system topologies, atom types, or other "real world"\nproperties.\n\nYou only need to provide atom coordinates, atom indices (for molecule,\ngroup, molecule selections etc.), and other parameters for functions.\n\nThus it aims to be more like numpy or scipy itself than a typical\nmacromolecular software library, except that the particular routines\nand functions are usually found in that context.\n\n** Installation\n\nGet it from PyPI:\n\n#+BEGIN_SRC bash\n  pip install geomm\n#+END_SRC\n\n\nOr you can get the latest:\n\n#+BEGIN_SRC bash\n\ngit clone https://github.com/ADicksonLab/geomm.git\ncd geomm\n\n# you need cython to compile\npip install cython\n\n# install it\npip install -e .\n\n#+END_SRC\n\n\n** Community\n\nDiscussion takes place on riot.im (#geomm:matrix.org) which is a slack-like app that works\non the Matrix protocol:\n[[https://riot.im/app/#/room/#geomm:matrix.org]]\n\n\nYou can also contact me directly:\n\nsamuel.lotz@salotz.info\n',
    'author': 'Samuel Lotz',
    'author_email': 'samuel.lotz@salotz.info',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.7',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
