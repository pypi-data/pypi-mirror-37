# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['wepy',
 'wepy.analysis',
 'wepy.boundary_conditions',
 'wepy.orchestration',
 'wepy.reporter',
 'wepy.reporter.wexplore',
 'wepy.resampling',
 'wepy.resampling.decisions',
 'wepy.resampling.distances',
 'wepy.resampling.resamplers',
 'wepy.runners',
 'wepy.util',
 'wepy.work_mapper']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'dill>=0.2.8,<0.3.0',
 'geomm>=0.1.2,<0.2.0',
 'h5py>=2.8,<3.0',
 'mdtraj>=1.9,<2.0',
 'networkx>=2',
 'numpy>=1.15,<2.0',
 'pandas>=0.23.4,<0.24.0']

entry_points = \
{'console_scripts': ['wepy = wepy.orchestration.cli:cli']}

setup_kwargs = {
    'name': 'wepy',
    'version': '0.9.5',
    'description': 'A Weighted Ensemble simulation framework in pure Python with a focus on molecular dynamics.',
    'long_description': '* Weighted Ensemble Python (wepy)\n\n\nModular implementation and framework for running weighted ensemble\nsimulations in pure python, where the aim is to have simple things\nsimple and complicated things possible. The latter being the priority.\n\nThe goal of the architecture is that it should be highly modular to\nallow extension, but provide a "killer app" for most uses that just\nworks, no questions asked.\n\nComes equipped with support for [[https://github.com/pandegroup/openmm][OpenMM]] molecular dynamics,\nparallelization using multiprocessing, the [[http://pubs.acs.org/doi/abs/10.1021/jp411479c][WExplore]] \nand REVO (Resampling Ensembles by Variance Optimization) resampling\nalgorithms, and an HDF5 file format and library for storing and\nquerying your WE datasets that can be used from the command line.\n\nThe deeper architecture of ~wepy~ is intended to be loosely coupled,\nso that unforeseen use cases can be accomodated, but tightly\nintegrated for the most common of use cases, i.e. molecular dynamics.\n\nThis allows freedom for fast development of new methods.\n\n** Community\n\nDiscussion takes place on riot.im (#wepy:matrix.org) which is a slack-like app that works\non the Matrix protocol:\n[[https://riot.im/app/#/room/#wepy:matrix.org]]\n\nYou can also contact me directly:\n\nsamuel.lotz@salotz.info\n\n** Installation\n\nWe are on pip now:\n#+BEGIN_SRC bash\n  pip install wepy\n#+END_SRC\n\nWhich will install most dependencies, except for OpenMM (which you\npotentially might not even need). To install it you can just use the\nomnia anaconda repository for the version you want.\n\n#+BEGIN_SRC bash\n  conda install -c omnia openmm\n#+END_SRC\n\n\nYou can always install from git as well for the latest:\n\n#+BEGIN_SRC bash\n  git clone https://github.com/ADicksonLab/wepy\n  cd wepy\n  pip install -e .\n#+END_SRC\n\n\nIf installation went alright you should have this command line\ninterface for working with orchestration available:\n\n#+BEGIN_SRC bash\n  wepy --help\n#+END_SRC\n\n** Getting Started\n\nUntil there is proper documentation there are a few examples here\n(https://github.com/ADicksonLab/wepy/tree/master/examples).\n\nThere is an example with a pair of Lennard-Jones particles that runs\non the reference implementation. This is the "Hello World" example and\nshould be your starting point.\n\nA more advanced (and interesting) example is a non-equilibrium\nunbinding WExplore simulation of the soluble epoxide hydrolase (sEH)\nprotein with the inhibitor TPPU, which was the subject of this paper:\n\nLotz and Dickson. 2018. JACS 140 (2) pp. 618-628 (DOI: 10.1021/jacs.7b08572)\n',
    'author': 'Samuel Lotz',
    'author_email': 'samuel.lotz@salotz.info',
    'url': 'https://gitlab.com/ADicksonLab/wepy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
