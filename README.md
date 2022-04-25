# Traj2NMR

NMR spectral predictions from molecular dynamics simulation trajectories


## Introduction

Traj2NMR is a Python module developed to streamline the computation of NMR observables from molecular dynamics trajectories.


## Installation

Python3.X and Python3.X-dev need to be installed first. If using Ubuntu 20.04, this is done by:

```shell
sudo apt-get install python3.8 python3.8-dev
```

Traj2NMR can now be installed by cloning the GitHub repository and running setup.py:

```shell
git clone https://github.com/weberdak/traj2nmr
cd traj2nmr
python setup.py install
```

Note that Traj2NMR can only be used on Linux operating systems due to it's dependance on SHIFTX2, PPM and SPARTA+ for computing chemical shifts. These must be installed separately and visible to your system $PATH. Full instructions the set these up are included in the docs directory (see next section). 


## Instructions

Usage instruction are currently being written using Sphinx under the docs folder. These HTML documents will eventually be served using GitHub pages, but for now they must be compiled. In the terminal:

```shell
cd docs
make html
```

Then load the docs/_build/index.html file to navigate through the documentation.


## Recommended Python Setup (Virtual Enviroment)

It is recommended, although not essential, to use a Python virtual environment. This because Traj2NMR requires several dependencies that you may not want installed to you root installation. This is also beneficial for users lacking root permisions. First, make sure Python3 and venv is installed:

```shell
sudo apt-get install python3.8 python3.8-dev python3.8-venv
```

Create a new virtual environment. I like to create is under a ~/Programs directory in a python-venv folder. I.e., 

```shell
mkdir -p ~/Programs/python-venv
cd ~/Programs/python-venv
python3.8 -m venv traj2nmr
```

Now make an alias in your .bashrc file as a shortcut for activating the environment. Add the following line and save:

```shell
alias traj2nmr='source ~/Programs/python-venv/traj2nmr/bin/activate'
```

Now activate the environment by typing "traj2nmr" in the terminal.

Clone and install Traj2NMR in your preferred location:

```shell
git clone https://github.com/weberdak/traj2nmr
cd traj2nmr
python setup.py install
```

Install Jupyter notebook into you virtual environment, then add your environment to the kernel:

```shell
pip install jupyter
pip install ipykernel
python -m ipykernel install --user --name=traj2nmr
```

You will now have the option to use the Traj2NMR environment when creating a new notebook.
