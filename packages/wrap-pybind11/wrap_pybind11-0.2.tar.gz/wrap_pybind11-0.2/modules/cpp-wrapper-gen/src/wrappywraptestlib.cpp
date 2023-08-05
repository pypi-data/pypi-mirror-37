// File: ./wrappywraptestlib.cpp
// Date: 2018-10-14
//
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;
using namespace pybind11::literals;

void wrapStringA(py::module &);
void wrapStringB(py::module &);
void wrapStringC(py::module &);

PYBIND11_MODULE(pywraptestlib, m) {
wrapStringA(m);
wrapStringB(m);
wrapStringC(m);
}
