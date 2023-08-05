# Semi-automatic calcium sparks detection software

IOCBIO Sparks is a cross-platform application for analysis and
detection of calcium sparks when imaged using confocal microscope line
scanning mode. 

IOCBIO Sparks is a free software released under the GNU General Public
License (GPL), see the file [`LICENSE`](LICENSE) for details. For any
other licenses, please contact the authors, as specified under
`Copyright` below.

## Installation

There are several ways to install the software. The application
requires python3.

For Linux, at present, installation using `pip` is recommended. It is
expected that `pip` soulution would work for Mac as well. 

For Windows, `conda` solution is recommended for users that don't have
Python installed already. Otherwise, if using other than Anaconda
Python, consider using `pip` solution.

### pip

To be able to install PyQt5 using pip, you have to use python3.5 or
higher. If not available in the system, you can replace `pip3` command
below with `python3 -m pip`.

To install published version, run

```
pip3 install --user iocbio.sparks
```
This will install all dependencies and it is expected to add a command `iocbio-sparks` into your `PATH`. 
If the command is missing after installation, check whether the default location
of `pip3` installation is in your path. For Linux, it should be `~/.local/bin`.

Its possible to install from Git repository directly:
```
pip3 install --user git+https://gitlab.com/iocbio/sparks
```

For development, use

```
pip3 install --user -e .
```

in the source directory. To install the current version from the source, use

```
pip3 install --user .
```

Note that `--user` is recommended to avoid messing up the system
packages.


### conda (Anaconda or Miniconda3)

Here, concise installation instructions are given. For illustrated
instructions with screenshots, see [Detailed Anaconda
instructions](docs/INSTALL.Anaconda.md)

#### Installation Anaconda

Install Anaconda Python environment by downloading it from
https://www.anaconda.com/ . The package uses Python 3 language, so,
the version supporting it should be installed. At the moment of
writing, its Python 3.6.

#### Installation of iocbio.sparks

For installation from GUI:
* Start Anaconda Navigator
* Add channels by clicking "Channels" on the main screen and adding: 
    * conda-forge
    * iocbio
* icon for `iocbio.sparks` application should appear on the main
  Anaconda Navigator. Click on its install for installation.
  
Please note, it may take several minutes to install the application due 
to its dependencies. 

For installation from CLI, start Anaconda Prompt. In the prompt, add channels:
```
conda config --append channels conda-forge
conda config --append channels iocbio
```
and install software
```
conda install -c iocbio iocbio-sparks
```
and you are all set.

For running iocbio.sparks in Windows, its possible to start it as an
application from Anaconda Navigator or, directly, from starting
`iocbio-sparks` in `Anaconda/Scripts` directory. For convinience, a
shortcut can be created on desktop or Start Menu by the user.


## Copyright

Copyright (C) 2018 Laboratory of Systems Biology, Department of
Cybernetics, School of Science, Tallinn University of Technology.

Authors:
* Martin Laasmaa
* Marko Vendelin

Contact: Marko Vendelin <markov@sysbio.ioc.ee>

Software license: the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version. See [`LICENSE`](LICENSE) for details
