[![Build Status](https://travis-ci.org/kmedian/threesplit.svg?branch=master)](https://travis-ci.org/kmedian/threesplit)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/kmedian/threesplit/master?urlpath=lab)

# threesplit
Three-way data split into training set, validation set, and test set.


## Installation
The `threesplit` [git repo](http://github.com/kmedian/threesplit) is available as [PyPi package](https://pypi.org/project/threesplit)

```
pip install threesplit
```


## Usage
Check the [examples](examples) folder for notebooks.


## Commands
* Check syntax: `flake8 --ignore=F401`
* Remove `.pyc` files: `find . -type f -name "*.pyc" | xargs rm`
* Remove `__pycache__` folders: `find . -type d -name "__pycache__" | xargs rm -rf`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`



## Support
Please [open an issue](https://github.com/kmedian/threesplit/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/kmedian/threesplit/compare/).
