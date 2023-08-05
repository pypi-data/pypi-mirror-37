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
['dill>=0.2.8,<0.3.0',
 'h5py>=2.8,<3.0',
 'networkx>=2',
 'numpy>=1.15,<2.0',
 'pandas>=0.23.4,<0.24.0']

entry_points = \
{'console_scripts': ['wepy = wepy.orchestration.cli:cli']}

setup_kwargs = {
    'name': 'wepy',
    'version': '0.9.0',
    'description': 'A Weighted Ensemble simulation framework in pure Python with a focus on molecular dynamics.',
    'long_description': '* Weighted Ensemble Python (wepy)\n\n\nModular implementation and framework for running weighted ensemble\nsimulations in pure python, where the aim is to have simple things\nsimple and complicated things possible. The latter being the priority.\n\nThe goal of the architecture is that it should be highly modular to\nallow extension, but provide a "killer app" for most uses that just\nworks, no questions asked.\n\nComes equipped with support for [[https://github.com/pandegroup/openmm][OpenMM]] molecular dynamics,\nparallelization using multiprocessing, the [[http://pubs.acs.org/doi/abs/10.1021/jp411479c][WExplore]] \nand REVO (Resampling Ensembles by Variance Optimization) resampling\nalgorithms, and an HDF5 file format and library for storing and\nquerying your WE datasets that can be used from the command line.\n\nThe deeper architecture of ~wepy~ is intended to be loosely coupled,\nso that unforeseen use cases can be accomodated, but tightly\nintegrated for the most common of use cases, i.e. molecular dynamics.\n\nThis allows freedom for fast development of new methods.\n\n** Community\n\nDiscussion takes place on riot.im (#wepy:matrix.org) which is a slack-like app that works\non the Matrix protocol:\n[[https://riot.im/app/#/room/#wepy:matrix.org]]\n\nYou can also contact me directly:\n\nsamuel.lotz@salotz.info\n\n** Installation\n\nWepy is still in beta but you can install by cloning this repository,\nswitching to the last release and installing with pip:\n\n#+BEGIN_SRC bash\n  git clone https://github.com/ADicksonLab/wepy\n  cd wepy\n  pip install -e .\n#+END_SRC\n\nPyPI and Anaconda repos are planned.\n\nThe only absolutely necessary dependencies are ~numpy~ and ~h5py~\nwhich are used in the core classes.\n\nOutside of the core classes there are a couple of dependencies which\nare needed for this distribution but not in general if you use ~wepy~ as\na library:\n- OpenMM (http://openmm.org/) (7.2 suggested)\n- pandas (https://pandas.pydata.org/)\n- mdtraj (http://mdtraj.org)\n- networkx >=2 (https://networkx.github.io/)\n- geomm (https://github.com/ADicksonLab/geomm)\n\nTo install these see their pages and the instructions below for geomm.\n\nThe default ~Runner~ is for ~OpenMM~ and should also be installed\nautomatically when following these instructions (defined in\n~setup.py~) although it is not necessary to use openmm when using ~wepy~\nas a library.\n\nCurrently, some things are still coupled to ~mdtraj~ and thus this is\nalso a dependency for some functionality, although this will be\nrelaxed in the future and replaced with a dependency on our nascent\nproject ~geomm~.\n\nTo install geomm:\n#+BEGIN_SRC bash\ngit clone https://github.com/ADicksonLab/geomm.git\ncd geomm\n# compile the cython modules\npython setup.py build_ext --inplace\n# install it\npip install -e .\n\n#+END_SRC\n\n\nThere are other uses for ~mdtraj~ such as export of trajectories to\nmdtraj trajectories, which will not be removed.\n\nPandas is used for outputting some data records, for which there is\nalways a non-pandas option.\n\nNetworkX is used in the WExplore resampler for the region tree and\nalso for the tree module for manipulating the walker cloning/merging\ntrees.\n\n** Roadmap\n\n- [X] Weighted Ensemble Layer\n  - [X] simulation manager\n- [X] Resampling sub-module\n  - [X] Random clone-merge resampler\n  - [X] WExplore\n  - [X] REVO\n- [X] OpenMM support\n- [X] HDF5 output and API\n- [ ] Command Line Interface\n- [ ] PyPI and Anaconda repositories\n\n\n** Getting Started\n\nThere are a few examples here (https://github.com/ADicksonLab/wepy/tree/master/examples).\n\nThere is an example with a pair of Lennard-Jones particles that runs\non the reference implementation. This is the "Hello World" example and\nshould be your starting point.\n\nA more advanced (and interesting) example is a non-equilibrium\nunbinding WExplore simulation of the soluble epoxide hydrolase (sEH)\nprotein with the inhibitor TPPU, which was the subject of this paper:\n\nLotz and Dickson. 2018. JACS 140 (2) pp. 618-628 (DOI: 10.1021/jacs.7b08572)\n\nBe sure to install the extra dependencies for the examples as above in\nthe installation instructions.\n\n** Architecture\n\nThe overall architecture of the project is broken into separate modules:\n- Simulation Management :: a framework for running simulations, needs:\n  - Runner :: module that implements whatever dynamics you want to run\n    - e.g.\n      - OpenMM\n  - Resampler :: the key functionality of the Weighted Ensemble\n                 resampling procedure is implemented here\n    - e.g.\n      - WExplore\n  - WorkMapper :: a function that implements the map function that\n                   allows for arbitrary methods of parallelization\n  - Reporter :: Responsible for the collection and saving of data from wepy runs\n    - e.g. HDF5 or plaintext\n  - BoundaryConditions :: describes and performs boundary condition\n       transformations as the simulation progresses\n  - simulation manager :: coordinates all of these components to run simulations\n\n- helper sub-modules will make the construction of new simulation\n  management modules easier and standardized\n- Application Layer :: This is a convenience layer for building the\n     CLI and perhaps high level functions for users to write their own\n     scripts\n',
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
