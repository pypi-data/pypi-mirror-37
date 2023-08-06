[![Build Status](https://travis-ci.org/kmedian/pctl_scale.svg?branch=master)](https://travis-ci.org/kmedian/pctl_scale)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/kmedian/pctl_scale/master?urlpath=lab)

# pctl_scale
Scale a variable into an open interval (0,1) whereas values within a given lower and upper percentile maintain a linear relation, and outlier saturate towards the interval limits.

This scaling functions was developed with **ratio-scale** data in mind 
(i.e. it has a natural zero value).


## Table of Contents
* [Installation](#installation)
* [Usage](#usage)
* [Commands](#commands)
* [Support](#support)
* [Contributing](#contributing)


## Installation
The `pctl_scale` [git repo](http://github.com/kmedian/pctl_scale) is available as [PyPi package](https://pypi.org/project/pctl_scale)

```
pip install pctl_scale
```


## Usage
Check the [examples](examples) folder for notebooks.


## Commands
* Check syntax: `flake8 --ignore=F401`
* Remove `.pyc` files: `find . -type f -name "*.pyc" | xargs rm`
* Remove `__pycache__` folders: `find . -type d -name "__pycache__" | xargs rm -rf`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`


## Debugging
* Notebooks to profile python code are in the [profile](profile) folder


## Support
Please [open an issue](https://github.com/kmedian/pctl_scale/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/kmedian/pctl_scale/compare/).
