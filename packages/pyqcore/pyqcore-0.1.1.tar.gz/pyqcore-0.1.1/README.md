![Logo](https://www.qcore.co.jp/assets/img/logo.png)

--------------------------------------------------------------------------------

PyQCore is a Python package that provides high speed machine learning Framework.  
  
Currently, This package is the client for QuantumCore Engine on AWS which supports prediction of time series data.

We are in an early-release beta. Expect some adventures and rough edges.

- [More about PyQCore](#more-about-pyqcore)
    - [About QuantumCore Engine](#about-quantumcore-engine)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Communication](#communication)
- [License](#license)

| System | > 3.5                                                                                                                               |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Linux  | [![Build Status](https://ci.pytorch.org/jenkins/job/pytorch-master/badge/icon)](https://ci.pytorch.org/jenkins/job/pytorch-master/) | [![Build Status](https://ci.pytorch.org/jenkins/job/pytorch-master/badge/icon)](https://ci.pytorch.org/jenkins/job/pytorch-master/) |
| macOS  | [![Build Status](https://ci.pytorch.org/jenkins/job/pytorch-master/badge/icon)](https://ci.pytorch.org/jenkins/job/pytorch-master/) | [![Build Status](https://ci.pytorch.org/jenkins/job/pytorch-master/badge/icon)](https://ci.pytorch.org/jenkins/job/pytorch-master/) |


## More about PyQCore

At a granular level, PyQcore is a library that consists of the following components:

| Component                             | Description                                                                                                    |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **pyqcore.client.SimpleQCoreClient**  | a client class that makes model on QuantumCore Engine                                                          |
| **pyqcore.examples.jpvow.load_jpvow** | a function that loads sample data by [UCI repository](https://archive.ics.uci.edu/ml/datasets/Japanese+Vowels) |

This library is enable to use the QuantumCore Engine in your codes. Also you need get license code from QuantumCore website to use this library.([QuantumCore Inc.](https://www.qcore.co.jp) )

### About QuantumCore Engine

QuantumCore Engine is developed by [QuantumCore Inc.](https://www.qcore.co.jp) This new model is 4Kx faster and lighter than previous LSTM or RNN model without GPU. Also you do not have to adjust parameters anymore.  
The Engine you use with this library is currently running on t2.micro on AWS ([check out the speck here](https://aws.amazon.com/ec2/instance-types/)).  
 The company also plans to impliment this algorithm on small edge computer.



## Installation
Installing PyQcore is not difficult. Just run the command below:

```
pip install pyqcore
```
Or clone this repository and run:

```
python setup.py install
```


## Getting Started

Refer our [sample scrpts](./docs/sample.py) or [tutorial notebook](./docs/tutorial1.ipynb).  
Make sure that you need get license code from [QuantumCore Inc.](https://www.qcore.co.jp)

## Communication
* GitHub issues: bug reports, feature requests, install issues, RFCs, thoughts, etc.
* Mailing List: please send any issue at [info-dev@qcore.co.jp](mailto:info-dev@qcore.co.jp)


## License

Copyright (c) 2018 QuantumCore Inc.
