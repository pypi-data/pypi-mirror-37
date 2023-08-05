# create-python-package
Initialize a new package using best practices as described by the [Python Packaging Authority (PyPA)](https://packaging.python.org/tutorials/packaging-projects/).

Perfect for beginners and experts alike!

```
> create-python-package mypackage
```

No more guesswork!

The file structure you're left with looks like this
```
mypackage/
├── LICENSE
├── README.md
├── activate-venv -> /private/tmp/mypackage/venv/bin/activate
├── mypackage
│   ├── __init__.py
│   └── main.py
└── setup.py
```

## Virtualenv ready to go!
Inside the directory you can run
```
source activate-venv
```
to activate an isolated Python environment that was created specifically for that package. To deactivate it, type
```
deactivate
```

To learn more about virtual environments, see [Creating Virtual Environments](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments).

## Install
My recommendation is to run the latest version of `create-python-package` with pipx rather than installing it and freezing the version on your system. This is because as new tools and practices are added to `create-python-package`, you will automatically be using them.

Install [pipx](https://github.com/cs01/pipx).

```
> pipx create-python-package mypackage  # runs latest version
```

If you really want to install it you can.
```
> pipx install create-python-package
```

Requires Python 3.6+.

## Credits
Inspired by [create-react-app](https://github.com/facebook/create-react-app)
