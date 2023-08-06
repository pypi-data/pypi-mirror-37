## NGS Utils

[![Build Status](https://travis-ci.org/vladsaveliev/NGS_Utils.svg?branch=master)](https://travis-ci.org/vladsaveliev/NGS_Utils)

[![Anaconda-Server Badge](https://anaconda.org/vladsaveliev/ngs_utils/badges/installer/conda.svg)](https://conda.anaconda.org/vladsaveliev/ngs_utils)

Helper code for [AstraZeneca](https://github.com/AstraZeneca-NGS) and [UMCCR](https://github.com/umccr) bioinfomatics projects 
(e.g. [NGS_Reporting](https://github.com/AstraZeneca-NGS/NGS_Reporting), [umccrise](https://github.com/umccr/umccrise)).

Contains only lightweight source without any reference or test data, so supposed to be small and can be safely used as 
a dependency in other projects.


### Installation

From source:

```
python setup.py install
```

For development:

```
pip install -e .
```

Stable conda package:

```
conda install -c vladsaveliev ngs_utils
```
