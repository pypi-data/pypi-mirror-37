#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace pybind11::literals;


void wrapStringA(py::module &);
void wrapStringB(py::module &);
void wrapStringC(py::module &);

PYBIND11_MODULE(pytestlib, m) {
    wrapStringA(m);
    wrapStringB(m);
    wrapStringC(m);
}