# NMRFAMsim
NMR spectral predictions from molecular dynamics simulation



## Installation

### System requirements

NMRFAMsim's dependence on external binaries limits it to being run only on Linux-based systems. The following is needed for installation and proper function:

* Python 2.7 and 3
* Python 3 Pip
* Git
* ShiftX2 (http://www.shiftx2.ca/download.html)
* PPM (http://spin.ccic.osu.edu/index.php/download)
* SPARTA+ (https://spin.niddk.nih.gov/bax/software/SPARTA+/)

The binaries of ShiftX2, PPM and SPARTA+ must be in your PATH environment variable. Further instructions for setting up the dependencies are included below.



### Quick installation

If you have all of the dependencies properly installed, the simply clone this repository and install:

```shell
git clone https://github.com/weberdak/nmrfamsim
sudo python setup.py install
```

or to install without root privileges:

```shell
python setup.py install --prefix ~/.local
```

This will also take care of the required [Python modules](requirements.txt) as well.



### Installing dependencies

If you are having difficulties setting up the dependencies, then you may be able to follow the following instructions. These directly relate to Ubuntu 20.04 and may need to be modified if using another version or Linux distribution.



#### Python3, Pip and Git

These are required by NMRFAMsim and installed to system by:

```shell
sudo apt-get install python3.8 python3-pip git
```



#### ShiftX2

ShiftX2 is a bit tricky as it requires Python 2.7 and Java to run, and modifications to the code to stop it from clashing with Python 3. First install Python2.7 and Java:

```shell
sudo apt-get install python2.7 default-jre
```

Now make a "Programs" folder in your home directory and go into it:

```shell
mkdir ~/Programs
cd ~/Programs
```

Get the latest ShiftX2 from the Wishart Lab (http://www.shiftx2.ca/download.html) and unpack it:

```shell
wget http://www.shiftx2.ca/download/shiftx2-v113-linux-20180808.tgz
tar -xzvf shiftx2-v113-linux-20180808.tgz
```

Go into the directory and change every occurrence of "python" in the code to "python2.7". This stops the computer from executed parts of the code in Python3 and causing it to crash:

```shell
cd shiftx2-linux
awk '{ gsub(/python/, "python2.7"); print }' shiftx2.py > temp && mv temp shiftx2.py
chmod +x shiftx2.py
```

Now finally add the directory to your PATH variable using your favourite text editor (mine is Vim):

```shell
vim ~/.bashrc
```

And add lines to the file:

```shell
export SHIFTX2_DIR=~/Programs/shiftx2-linux
export PATH=$PATH:$SHIFTX2_DIR
```

For new Linux users, the .bashrc file is loaded whenever you open a BASH terminal. The PATH variable tells the terminal what directories contain executable binaries and scripts (i.e., installed programs). Once added to the PATH, "shiftx2.py" can now be executed from any folder on your system.



#### PPM

PPM is relatively simple to install and is pretty much ready to use once it is unpacked and added to the PATH. However, it does require OpenMP to run:

```shell
sudo apt-get install libomp-dev
```

Download the archive file [ppm_linux.tar](http://spin.ccic.osu.edu/index.php/download) from Oregon State University NMR website and copy it into the Programs directory. Then:

```shell
cd ~/Programs
mkdir ppm_linux
tar -xvf ppm_linux.tar -C ppm_linux
```

And add/modify the following lines of your ~/.bashrc file:

```shell
export SHIFTX2_DIR=~/Programs/ppm_linux
export PATH=$PATH:$SHIFTX2_DIR:$PPM_DIR
```



#### SPARTA+

SPARTA+ installation does not very much from what is described on the website. However, we will be adding in to our BASH terminal rather than CSH/TCSH so that is visible to NMRFAMsim. Although, CSH or TCSH is still needed for installation:

```shell
sudo apt-get install tcsh
```

Go into the Programs directory, get [SPARTA+](https://spin.niddk.nih.gov/bax/software/SPARTA+/) from the Bax Lab and unpack: 

```shell
cd ~/Programs
wget http://spin.niddk.nih.gov/bax/software/SPARTA+/sparta+.tar.Z
tar -zxvf sparta+.tar.Z
```

Allow the install.com script to run as an executable and install:

```shell
cd SPARTA+
chmod +x install.com
./install.com
```

Now add SPARTA+ to your PATH in your ~/.bashrc:

```shell
export SPARTAP_DIR=~/Programs/SPARTA+
export PATH=$PATH:$SHIFTX2_DIR:$PPM_DIR:$SPARTAP_DIR/bin
```

Note that the variable must be called "SPARTAP_DIR", otherwise SPARTA+ won't work.




### Using Docker and Docker Compose

If users are having difficulties with configuring all the dependencies, it might be worth considering using Docker. This repository contains a [Dockerfile](Dockerfile) that essentially builds a basic Linux container on your system with all the required dependencies configured correctly. This container is based on the [Miniconda3 image](https://hub.docker.com/r/continuumio/miniconda3) and is spun up on your system using the [docker-compose.yml](docker-compose.yml) file for Docker Compose. To use this method:

1. Install [Docker](https://docs.docker.com/engine/install/ubuntu/) and [Docker-Compose](https://docs.docker.com/compose/install/) on your machine. This require root permissions and probably assistance from your IT department. Once installed, configure your user account to [run Docker without root permissions](https://docs.docker.com/engine/install/linux-postinstall/) - regardless of whether you have them already or not.

2. Install Git:

	```shell
	sudo apt-get install git
	```

3. Clone NMRFAMsim repository onto your machine

	```shell
	git clone https://github.com/weberdak/nmrfamsim
	cd nmrfamsim
	```

4. Make a "dependencies" folder to download ShiftX2, Sparta+ and PPM into. The "data" folder is also created as a working directory for the container once started up:

   ```shell
   mkdir dependencies data
   cd dependencies
   ```

5. Download the archive for ShiftX2 ([shiftx2-v113-linux-20180808.tgz](http://www.shiftx2.ca/download/shiftx2-v113-linux-20180808.tgz)) into the dependencies folder or use wget:

   ```shell
   wget http://www.shiftx2.ca/download/shiftx2-v113-linux-20180808.tgz
   ```

6. Download the archive for SPARTA+ ([sparta+.tar.Z](https://spin.niddk.nih.gov/bax/software/SPARTA+/)) into the dependencies folder or use wget:

	```shell
	wget http://spin.niddk.nih.gov/bax/software/SPARTA+/sparta+.tar.Z
	```

7. Download the archive for PPM ([ppm_linux.tar](http://spin.ccic.osu.edu/index.php/download)) into the dependencies folder. If the archive file name differs for either of these packages, the [Dockerfile](Dockerfile) will have to be modified accordingly.
8. Now build the Docker container:

   ```shell
   docker-compose build
   ```

9. And start up the container by:

	```shell
	docker-compose up
	```
	
10. Once the container is started, you can use NMRFAMsim via the Jupyter Notebook exposed on port 8888 by entering the URL https://localhost:8888/ into your browser. Ignore the security warning as it relates to the self-signed SSL certificate used withing the container, which is unimportant since you are running the container on your own system. Copy any input files into the "data" folder as it is the working directory and is shared between the host system and the container. Note that the NMRFAMsim code cloned from GitHub is also mounted and shared with the container, and can be developed on the host system without having to rebuild the container each time an edit is made.

11. To shut down the container gracefully, press Ctrl+C and:

    ```shell
    docker-compose down
    ```

12. Occasionally your system might become a bit clogged with old Docker containers. In this case, it might be useful to wipe Docker clean by the following and rebuilding from scratch:

	```shell
	docker stop $(docker ps -a -q)
	docker rm $(docker ps -a -q)
	docker rmi $(docker images -a -q)
	```
