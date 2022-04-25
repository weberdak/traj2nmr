
.. _installation:

Installation
============

This page explains how Traj2NMR and it's dependencies are installed. Note that Traj2NMR contains wrappers for chemical shift prediction programs SHIFTX2, SPARTA+ and PPM, which need to be installed and in your PATH. Instructions for installing these packages are also detailed here. These packages also restrict Traj2NMR to running only on Linux operating systems.


From GitHub
-----------

Simply clone (or download) the Traj2NMR repository and install by:

.. code-block:: shell

    git clone https://github.com/weberdak/traj2nmr
    python setup.py install


Dependencies
------------

Traj2NMR requires external modules for computing chemical shifts. These are run by Traj2NMR first writing temporary input files to disk (i.e., PDB files for each frame of the trajectory saved to a hidden folder), the specified program is executed, and then the output files are read into Traj2NMR in the required data structure. It is recommended that SHIFTX2 is at least installed since it is the only one capable of computing both backbone and sidechain chemical shifts. However, SHIFTX2 is by far the slowest (~hours required to process a trajectory). Therefore, users may wish to compute backbone shifts for all frames (higher accuracy) using the faster PPM or SPARTA+ programs, and using SHIFTX2 to compute sidechain shifts from a smaller subset of frames.


SHIFTX2
```````

ShiftX2 is a bit tricky as it requires Python 2.7 and Java to run, and modifications to the code to prevent clashes with Python 3. First install Python2.7 and Java:

.. code-block:: shell

    sudo apt-get install python2.7 default-jre

Now make a "Programs" folder in your home directory and go to it:

.. code-block:: shell

    mkdir ~/Programs
    cd ~/Programs

Note that the directory does not need to be "Programs", we just use it here as an example. Get the latest ShiftX2 from the Wishart Lab (http://www.shiftx2.ca/download.html) and unpack it:

.. code-block:: shell

    wget http://www.shiftx2.ca/download/shiftx2-v113-linux-20180808.tgz
    tar -xzvf shiftx2-v113-linux-20180808.tgz

Go into the directory and change every occurrence of "python" in the code to "python2.7" using the following Awk command:

.. code-block:: shell

    cd shiftx2-linux
    awk '{ gsub(/python/, "python2.7"); print }' shiftx2.py > temp && mv temp shiftx2.py
    chmod +x shiftx2.py

If this is not done, the script will execute these lines with Python 3.X and crash. Now finally add the directory to your PATH variable using a text editor (i.e., vim):

.. code-block:: shell

    vim ~/.bashrc

And add lines to the file:

.. code-block:: shell

    export SHIFTX2_DIR=~/Programs/shiftx2-linux
    export PATH=$PATH:$SHIFTX2_DIR

For new Linux users, the .bashrc file is loaded whenever you open a BASH terminal. The PATH variable tells the terminal what directories contain executable binaries and scripts (i.e., installed programs). Once added to the PATH, "shiftx2.py" can now be executed from any folder on your system.


SPARTA+
```````

Install as per the Bax Lab website. First install TCSH:

.. code-block:: shell

    sudo apt-get install tcsh

Go to the Programs directory, get SPARTA+(https://spin.niddk.nih.gov/bax/software/SPARTA+/) from the Bax Lab and unpack: 

.. code-block:: shell

    cd ~/Programs
    wget http://spin.niddk.nih.gov/bax/software/SPARTA+/sparta+.tar.Z
    tar -zxvf sparta+.tar.Z

Change install.com script permission to executable and use it to install SPARTA+:

.. code-block:: shell

    cd SPARTA+
    chmod +x install.com
    ./install.com

Now add SPARTA+ to your PATH in your ~/.bashrc:

.. code-block:: shell

    export SPARTAP_DIR=~/Programs/SPARTA+
    export PATH=$PATH:$SHIFTX2_DIR:$PPM_DIR:$SPARTAP_DIR/bin

Note that the variable must be called "SPARTAP_DIR", otherwise SPARTA+ won't work. Note SPARTA+ is typically run from the CSH or TCSH environment, which is not visible to Traj2NMR (only the BASH environment is visable).


PPM
```

PPM is relatively simple to install. However, first install OpenMP:

.. code-block:: shell

    sudo apt-get install libomp-dev

Download the archive file "ppm_linux.tar" (http://spin.ccic.osu.edu/index.php/download) from Oregon State University NMR website and copy it into the Programs directory. Then:

.. code-block:: shell

    cd ~/Programs
    mkdir ppm_linux
    tar -xvf ppm_linux.tar -C ppm_linux

And add/modify the following lines of your ~/.bashrc file:

.. code-block:: shell

    export PPM_DIR=~/Programs/ppm_linux
    export PATH=$PATH:$SHIFTX2_DIR:$PPM_DIR