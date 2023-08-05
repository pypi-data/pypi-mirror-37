#!/bin/bash
python ../../../wrap_pybind11/WrapPybind11Exec.py --export_json --module_name pywraptestlib --header_paths ../../cpp-stl-example-vec-string/include/StringA.h,../../cpp-stl-example-vec-string/include/StringB.h,../../cpp-stl-example-vec-string/include/StringC.h
#