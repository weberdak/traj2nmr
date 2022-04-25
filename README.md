# NMRFAMsim
NMR spectral predictions from molecular dynamics simulation trajectories


## Introduction

Traj2NMR is a Python module developed to streamline the computation of NMR observables from molecular dynamics trajectories.


## Installation

Python3.X and Python3.X-dev need to be installed first. If using Ubuntu 20.04, this is done by:

```shell
sudo apt-get install python3.8 python3.8-dev
```

Note that Traj2NMR can only be used on Linux operating systems due to it's dependance on SHIFTX2, PPM and SPARTA+ for computing chemical shifts.

Traj2NMR can now be installed by cloning the GitHub repository and running setup.py:

```shell
git clone https://github.com/weberdak/traj2nmr
cd traj2nmr
python setup.py install
```


## Instructions

Usage instruction are currently being written using Sphinx under the docs folder. These HTML documents will eventually be served using GitHub pages, but for now they must be compiled. In the terminal:

```shell
cd docs
make html
```

Then load the docs/_build/index.html file to navigate through the documentation.