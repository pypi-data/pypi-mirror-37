# Parallel Asynchronous Remote Optimization

[![Documentation Status](https://readthedocs.org/projects/paryopt/badge/?version=latest)](https://paryopt.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://baskar-group.me.iastate.edu/jenkins/buildStatus/icon?job=PARyOpt)](https://baskar-group.me.iastate.edu/jenkins/job/PARyOpt/)


This framework performs Asynchronous Bayesian Optimization with support for remote evaluations, resilient to hardware/software failures

Documentation for the software is available [here](http://paryopt.readthedocs.io)


![1d example](bo_animation.gif =100x20)

### How do I get set up? ###

This code is compatible with Python3.5, and requires several modules. The requirements are available in `requirements.txt`. If you are doing a tar ball installation, do

```
python3.5 install -r requirements.txt
python3.5 install setup.py

```

If you are using a pip installation, simply do

```
python3.5 -m pip install paryopt
```

The publication related to the implementation can be found [here](https://arxiv.org/pdf/1809.04668). 

### Who do I talk to? ###

[Balaji Pokuri](mailto:balajip@iastate.edu)

[Alec Lofquist](mailto:lofquist@iastate.edu)

[Baskar Ganapathysubramanian](mailto:baskarg@iastate.edu)
