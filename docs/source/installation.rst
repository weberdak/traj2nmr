
.. _installation:

Installation instructions
=========================

Basic installation
------------------

Python3.X and Python3.X-dev need to be installed first. If using Ubuntu 20.04, this can be done by:

.. code-block:: shell
    
    $ sudo apt-get install python3.8 python3.8-dev

Traj2NMR, including Python dependencies, can then be installed by cloning the repository and running setup.py:

.. code-block:: shell

    $ git clone https://github.com/weberdak/traj2nmr
    $ cd traj2nmr
    $ python setup.py install

Note that Traj2NMR can only be used on Linux operating systems due to it's dependance on SHIFTX2, PPM and SPARTA+ for chemical shift predictions. These must be installed separately and added to your $PATH variable. Full instructions for this are included below. 


Setup using a Python virtual environment (recommended)
------------------------------------------------------

It is recommended, although not essential, to use a Python virtual environment. This is because Traj2NMR requires several dependencies that you may not want installed to your root Python installation. First, make sure Python3 and virtual environments are installed. I.e., on Ubuntu 20.04:

.. code-block:: shell

    $ sudo apt-get install python3.8 python3.8-dev python3.8-venv

Create a new virtual environment. For example, I like to create these under a ~/Programs directory in a python-venv subfolder:

.. code-block:: shell

    $ mkdir -p ~/Programs/python-venv
    $ cd ~/Programs/python-venv
    $ python3.8 -m venv traj2nmr

Now make an alias in your ~/.bashrc file as a shortcut for activating the environment. Add the following line:

.. code-block:: shell

    alias traj2nmr='source ~/Programs/python-venv/traj2nmr/bin/activate'

Now you can activate the environment simply by typing "traj2nmr" into terminal. With the traj2nmr environment activated, clone and install Traj2NMR within your preferred folder:

.. code-block:: shell

    $ git clone https://github.com/weberdak/traj2nmr
    $ cd traj2nmr
    $ python setup.py install

Traj2NMR is most likely to be used via a Jupyter Notebook, in which case the new Python environment will need to be added to the underlying iPython kernel. To do this, with the traj2nmr environment still activated, install Jupyter notebook and then add the environment to the kernel:

.. code-block:: shell

    $ pip install jupyter
    $ pip install ipykernel
    $ python -m ipykernel install --user --name=traj2nmr

You will now have the option to use the Traj2NMR environment when creating a new notebook.


Installation of dependencies
----------------------------

Traj2NMR requires external programs for computing chemical shifts. These can be installed as per the following instructions.


SHIFTX2
```````

ShiftX2 is a bit tricky as it requires Python 2.7 and Java to run, and modifications to the code to prevent clashes with Python 3. First install Python2.7 and Java:

.. code-block:: shell

    $ sudo apt-get install python2.7 default-jre

Now make a "Programs" folder in your home directory and go to it:

.. code-block:: shell

    $ mkdir ~/Programs
    $ cd ~/Programs

Note that the directory does not need to be "Programs", we just use it here as an example. Get ShiftX2 from the Wishart Lab website (http://www.shiftx2.ca/download.html) and unpack it:

.. code-block:: shell

    $ wget http://www.shiftx2.ca/download/shiftx2-v113-linux-20180808.tgz
    $ tar -xzvf shiftx2-v113-linux-20180808.tgz

Go into the directory and change every occurrence of "python" in the code to "python2.7" using the following Awk command:

.. code-block:: shell

    $ cd shiftx2-linux
    $ awk '{ gsub(/python/, "python2.7"); print }' shiftx2.py > temp && mv temp shiftx2.py
    $ chmod +x shiftx2.py

If this is not done, the script will execute these lines with Python 3.X and crash. Now add the directory to your PATH variable, in the ~/.bashrc file, using your preferred text editor. For example, add the following lines and save:

.. code-block:: shell

    export SHIFTX2_DIR=~/Programs/shiftx2-linux
    export PATH=$PATH:$SHIFTX2_DIR


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

Set executable permission for the install.com script an run it:

.. code-block:: shell

    $ cd SPARTA+
    $ chmod +x install.com
    $ ./install.com

Now add SPARTA+ to your PATH in your ~/.bashrc:

.. code-block:: shell

    export SPARTAP_DIR=~/Programs/SPARTA+
    export PATH=$PATH:$SHIFTX2_DIR:$PPM_DIR:$SPARTAP_DIR/bin

Note that the variable must be called "SPARTAP_DIR", otherwise SPARTA+ won't work. Note SPARTA+ is typically run from the CSH or TCSH environment, which is not visible to Traj2NMR (only the BASH environment is visible).


PPM
```

PPM is relatively simple to install. However, you must first install OpenMP:

.. code-block:: shell

    $ sudo apt-get install libomp-dev

Download the archive file "ppm_linux.tar" (http://spin.ccic.osu.edu/index.php/download) from Oregon State University NMR website and copy it into the Programs directory. Then:

.. code-block:: shell

    $ cd ~/Programs
    $ mkdir ppm_linux
    $ tar -xvf ppm_linux.tar -C ppm_linux

Then add/modify the following lines of your ~/.bashrc file:

.. code-block:: shell

    export PPM_DIR=~/Programs/ppm_linux
    export PATH=$PATH:$SHIFTX2_DIR:$PPM_DIR