
.. _installation:

Installation
============

This page explains how Traj2NMR and it's dependencies are installed. Note that Traj2NMR contains wrappers for chemical shift prediction programs SHIFTX2, SPARTA+ and PPM, which need to be installed and in your PATH. Instructions for installing these packages are also detailed here. These packages also restrict Traj2NMR to running only on Linux operating systems.


Basic setup
-----------

Python3.X and Python3.X-dev need to be installed first. If using Ubuntu 20.04, this is done by:

.. code-block:: shell
    
    $ sudo apt-get install python3.8 python3.8-dev

Traj2NMR, including Python dependencies, can then be installed by cloning the GitHub repository and running setup.py:

.. code-block:: shell

    $ git clone https://github.com/weberdak/traj2nmr
    $ cd traj2nmr
    $ python setup.py install

Note that Traj2NMR can only be used on Linux operating systems due to it's dependance on SHIFTX2, PPM and SPARTA+ for computing chemical shifts. These must be installed separately and visible to your system $PATH. Full instructions for this are included in the next section. 


Setup using a Python virtual environment (recommended)
------------------------------------------------------

It is recommended, although not essential, to use a Python virtual environment. This is because Traj2NMR requires several dependencies that you may not want installed to your root installation. First, make sure Python3 and virtual environments are installed:

.. code-block:: shell

    $ sudo apt-get install python3.8 python3.8-dev python3.8-venv

Create a new virtual environment. For example, I like to create is under a ~/Programs directory in a python-venv folder:

.. code-block:: shell

    $ mkdir -p ~/Programs/python-venv
    $ cd ~/Programs/python-venv
    $ python3.8 -m venv traj2nmr

Now make an alias in your ~/.bashrc file as a shortcut for activating the environment. Add the following line and save:

.. code-block:: shell

    alias traj2nmr='source ~/Programs/python-venv/traj2nmr/bin/activate'

Now activate the environment by typing "traj2nmr" in the terminal. As per the basic setup, clone and install Traj2NMR in your preferred folder:

.. code-block:: shell

    $ git clone https://github.com/weberdak/traj2nmr
    $ cd traj2nmr
    $ python setup.py install

Traj2NMR is most likely to used via Jupyter Notebook, in which case this new Python environment will need to be added to the underlying iPython kernel. To do this, with the traj2nmr environment activated, install Jupyter notebook then add the environment to the kernel:

.. code-block:: shell

    $ pip install jupyter
    $ pip install ipykernel
    $ python -m ipykernel install --user --name=traj2nmr

You will now have the option to use the Traj2NMR environment when creating a new notebook.


Dependencies
------------

Traj2NMR requires external modules for computing chemical shifts. These are run by Traj2NMR first writing temporary input files to disk (i.e., PDB files for each frame of the trajectory saved to a hidden folder), the specified program is executed, and then the output files are read into Traj2NMR in the required data structure. It is recommended that SHIFTX2 is at least installed since it is the only one capable of computing both backbone and sidechain chemical shifts. However, SHIFTX2 is by far the slowest (~hours required to process a trajectory). Therefore, users may wish to compute backbone shifts for all frames (higher accuracy) using the faster PPM or SPARTA+ programs, and using SHIFTX2 to compute sidechain shifts from a smaller subset of frames.


SHIFTX2
```````

ShiftX2 is a bit tricky as it requires Python 2.7 and Java to run, and modifications to the code to prevent clashes with Python 3. First install Python2.7 and Java:

.. code-block:: shell

    $ sudo apt-get install python2.7 default-jre

Now make a "Programs" folder in your home directory and go to it:

.. code-block:: shell

    $ mkdir ~/Programs
    $ cd ~/Programs

Note that the directory does not need to be "Programs", we just use it here as an example. Get the latest ShiftX2 from the Wishart Lab (http://www.shiftx2.ca/download.html) and unpack it:

.. code-block:: shell

    $ wget http://www.shiftx2.ca/download/shiftx2-v113-linux-20180808.tgz
    $ tar -xzvf shiftx2-v113-linux-20180808.tgz

Go into the directory and change every occurrence of "python" in the code to "python2.7" using the following Awk command:

.. code-block:: shell

    $ cd shiftx2-linux
    $ awk '{ gsub(/python/, "python2.7"); print }' shiftx2.py > temp && mv temp shiftx2.py
    $ chmod +x shiftx2.py

If this is not done, the script will execute these lines with Python 3.X and crash. Now finally add the directory to your PATH variable using a text editor (i.e., vim):

.. code-block:: shell

    $ vim ~/.bashrc

And add lines to the file:

.. code-block:: shell

    export SHIFTX2_DIR=~/Programs/shiftx2-linux
    export PATH=$PATH:$SHIFTX2_DIR

For new Linux users, the .bashrc file is loaded whenever you open a BASH terminal. The PATH variable tells the terminal what directories contain executable binaries and scripts (i.e., installed programs). Once added to the PATH, "shiftx2.py" can now be executed from any folder on your system.


SPARTA+
```````

Install as per the Bax Lab website. First install TCSH:

.. code-block:: shell

    $ sudo apt-get install tcsh

Go to the Programs directory, get SPARTA+(https://spin.niddk.nih.gov/bax/software/SPARTA+/) from the Bax Lab and unpack: 

.. code-block:: shell

    $ cd ~/Programs
    $ wget http://spin.niddk.nih.gov/bax/software/SPARTA+/sparta+.tar.Z
    $ tar -zxvf sparta+.tar.Z

Change install.com script permission to executable and use it to install SPARTA+:

.. code-block:: shell

    $ cd SPARTA+
    $ chmod +x install.com
    $ ./install.com

Now add SPARTA+ to your PATH in your ~/.bashrc:

.. code-block:: shell

    export SPARTAP_DIR=~/Programs/SPARTA+
    export PATH=$PATH:$SHIFTX2_DIR:$PPM_DIR:$SPARTAP_DIR/bin

Note that the variable must be called "SPARTAP_DIR", otherwise SPARTA+ won't work. Note SPARTA+ is typically run from the CSH or TCSH environment, which is not visible to Traj2NMR (only the BASH environment is visable).


PPM
```

PPM is relatively simple to install. However, first install OpenMP:

.. code-block:: shell

    $ sudo apt-get install libomp-dev

Download the archive file "ppm_linux.tar" (http://spin.ccic.osu.edu/index.php/download) from Oregon State University NMR website and copy it into the Programs directory. Then:

.. code-block:: shell

    $ cd ~/Programs
    $ mkdir ppm_linux
    $ tar -xvf ppm_linux.tar -C ppm_linux

And add/modify the following lines of your ~/.bashrc file:

.. code-block:: shell

    export PPM_DIR=~/Programs/ppm_linux
    export PATH=$PATH:$SHIFTX2_DIR:$PPM_DIR