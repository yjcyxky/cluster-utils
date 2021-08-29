# cluster-utils

The Choppy Cluster Utilities are the basic file, shell and text manipulation utilities of the GNU operating system and HPC Cluster. These are the cluster utilities which are expected to exist on every operating system or HPC Cluster.

## Prerequirement

Install environment-modules(Provides dynamic modification of a user's environment)

  ```bash
  # For CentOS
  yum install epel-release
  yum install environment-modules

  # For Ubuntu
  apt-get update
  apt-get install environment-modules
  ```

## Usage

**NOTE: We assume you would like to install cluster-utils in /opt/local/ directory**

1. Clone the repo to your local machine
   
  ```
  cd /opt/local
  git clone https://github.com/go-choppy/cluster-utils
  ```

2. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links) / Anaconda

  ```bash
  # Based on the version of your python interpreter

  # Python2? Need to install python3 firstly.
  yum install python3

  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

  bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/local/cluster-utils/miniconda3
  ```   

3. Set PATH variable, **e.g. cluster-utils in /opt/local/cluster-utils directory**.
   
  ```
  echo "export PATH=/opt/local/cluster-utils/bin:/opt/local/cluster-utils/miniconda3/bin:$PATH" >> /etc/bashrc
  source ~/.bashrc
  ```

4. Set MODULEPATH to /opt/local/cluster-utils/share/modulefiles
   
  ```
  echo "export MODULEPATH=/opt/local/cluster-utils/share/modulefiles:$MODULEPATH" >> /etc/bashrc
  source ~/.bashrc
  ```

5. Use cobweb to manage your softwares
   
  ```
  cobweb -h
  ```