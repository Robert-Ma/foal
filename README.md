**Quick Install:**
```sh
$ pip3 install -e git+https://github.com/Robert-Ma/foal.git#egg=foal
```
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Introduction](#introduction)
- [Install](#install)
    - [Uninstall](#uninstall)
- [Usage](#usage)
- [Update](#update)
- [License](#license)

<!-- markdown-toc end -->

# Introduction

This package is designed to implement some basic algorithms using **Python3**. 
**_Note_** that these implementations are __*not optimized*__.
If performance is very important, please search for related packages 
in [pypi](https://pypi.org). In fact, this package is only used to **practice** python3. 

# Install

1. You can install this automatically:

``` sh
$ pip3 install -e git+https://github.com/Robert-Ma/foal.git#egg=foal
```

2. Or install manually:

first, download this repository, and follow:

``` sh
$ cd /path/to/foal.tar
$ pip3 install ./foal.tar
```

## Uninstall

Uninstall this package:

``` sh
$ pip3 uninstall foal
```

# Usage

``` python3
import foal
import foal.Search
import foal.Sort
```

# Update

Update this package using pip3:

``` sh
$ pip3 install -e -U git+https://github.com/Robert-Ma/foal.git#egg=foal
```

# License

The license is [MIT](https://choosealicense.com/licenses/mit/).
