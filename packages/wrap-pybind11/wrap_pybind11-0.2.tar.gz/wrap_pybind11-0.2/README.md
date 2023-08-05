## Python C++ Wrapper Tools using PyBind11

### Introduction

wrap_pybind11 is simple utility to create python wrappers for C++ modules
using the [PyBind11](https://github.com/pybind/pybind11) header library.
This tool was created to specifically address the coding styles and conventions
for the RCSB/PDB project C++ data processing libraries.

Other tools in this space include [PyBind11Gen](https://github.com/virtuald/pybind11gen) and
the very comprehensive [binder](https://github.com/RosettaCommons/binder) package from the Rosetta Project.


### Installation

Installation is via the program [pip](https://pypi.python.org/pypi/pip).

```bash
pip install wrap_pybind
```

```bash
wrap_pybind_cli --h

usage: WrapPybind11Exec.py [-h] [--module_name MODULENAME]
                           [--header_paths HEADERPATHLIST]
                           [--class_exclude CLASSEXCLUDELIST]
                           [--output_path OUTPUTPATH] [--export_json]

optional arguments:

  -h, --help            show this help message and exit

  --module_name MODULENAME
                        Module name

  --header_paths HEADERPATHLIST
                        Header paths (comma separated list)

  --class_exclude CLASSEXCLUDELIST
                        Class name exclude list (comma separated list)

  --output_path OUTPUTPATH
                        Output path for wrapped code

  --export_json         Output path for wrapped code

```

From the source module, the install is as follows:

```bash

git clone --recurse-submodules https://github.com/rcsb/py-wrap_pybind11.git

cd py-wrap_pybind11
python setup.py build
python setup.py install

or

# Simple C++ test classes are in modules/cpp-stl-example-vec-string

# To create the test wrapper source files for these examples
cd modules/cpp-wrapper/src
./Run.sh

# Then build wrapper library -
cd ../../..
./BUILD.sh  # runs cmake

# Test the wrapper library -
cd tests
python PyWrapLibTests.py

```