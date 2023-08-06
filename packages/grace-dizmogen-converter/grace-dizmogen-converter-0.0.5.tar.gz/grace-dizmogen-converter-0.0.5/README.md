# Grace To dizmoGen Converter

This simple script converts an existing grace dizmo into a dizmoGen dizmo. It requires dizmoGen (but not Grace) to be available on the system.

# Requirements

* Python3
* npm - \@dizmo/generator-dizmo

# Installation

## Linux/MacOS

The preferred way of installing dizmogen_converter is to make use of Python's virtual environment.
```
python3 -m venv .venv
source .venv/bin/activate
pip install grace-dizmogen-converter
```

If you rather install it globally you can do so, but you will need superuser privileges:
```
sudo pip3 install grace-dizmogen-converter
```

## Windows

There is currently no easy installer for windows. If you have a complete python environment set up it is the same as on linux/mac, otherwise you can always make use of the linux subsytem for windows.

# Usage

To use the converter, navigate into a Grace dizmo directory and execute `dizmogen_converter`. This will create a new directory inside the parent directory of the current directory with the converted dizmo.

Example (with source to .venv, only use this if you are using a virtual env.):
```
$ cd some_grace_dizmo
$ dizmogen_converter
$ cd ../some_grace_dizmo__converter
$ npm install
```
