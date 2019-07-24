# cluster-utils

The Choppy Cluster Utilities are the basic file, shell and text manipulation utilities of the GNU operating system and HPC Cluster. These are the cluster utilities which are expected to exist on every operating system or HPC Cluster.

## Prerequirement
1. Install Miniconda / Anaconda
2. Install environment-modules(Provides dynamic modification of a user's environment)

## Usage
1. Clone the repo to your local machine
```
git clone https://github.com/go-choppy/cluster-utils
```

2. Set PATH variable, e.g. cluster-utils in ~/softwares directory.
```
echo "export PATH=~/softwares/cluster-utils/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
```

3. Set MODULEPATH to ~/softwares/cluster-utils/share/modulefiles

4. Use cobweb to manage your softwares
```
cobweb -h
```