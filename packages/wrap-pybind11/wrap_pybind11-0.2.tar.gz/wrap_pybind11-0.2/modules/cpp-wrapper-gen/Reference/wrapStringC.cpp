// File: wrapStringC.cpp
//
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <string>

#include "StringC.h"

namespace py = pybind11;
using namespace pybind11::literals;

//PYBIND11_MAKE_OPAQUE(std::vector<std::string>);

void wrapStringC(py::module &m) {
    m.doc() = "Wrapper test example for strings and vectors";

    py::class_<StringC> cls(m, "StringC", "STL String and Vector test cases");
        //py::handle cl_type = cls;
        py::enum_<StringC::eCompareTypeC>(cls,"eCompareTypeC")
            .value("eCASE_SENSITIVE", StringC::eCompareTypeC::eCASE_SENSITIVE)
            .value("eCASE_INSENSITIVE", StringC::eCompareTypeC::eCASE_INSENSITIVE)
            .value("eWS_INSENSITIVE", StringC::eCompareTypeC::eWS_INSENSITIVE)
            .value("eAS_INTEGER", StringC::eCompareTypeC::eAS_INTEGER)
            .export_values();
        cls.def(py::init<>());
        cls.def(py::init<double>(), py::arg("dVal"));
        cls.def(py::init<int>(), py::arg("dVal"));
        cls.def(py::init<std::string>(), py::arg("name"));
        cls.def(py::init<std::string, StringC::eCompareTypeC>(), py::arg("name"), py::arg("eCase"));
        // overloaded examples -
        cls.def("setStuff", (void (StringC::*)(int)) &StringC::setStuff, "Setstuff int", py::arg("newIndex"));
        cls.def("setStuff", (void (StringC::*)(double)) &StringC::setStuff, "Setstuff double", py::arg("dVal"));
        cls.def("setStuff", (void (StringC::*)(int, double)) &StringC::setStuff, "Setstuff int and double", py::arg("newIndex"), py::arg("dVal"));
        cls.def("setStuff", (void (StringC::*)(int, double, const StringC::eCompareTypeC )) &StringC::setStuff, "Setstuff int and double,enum", py::arg("newIndex"), py::arg("dVal"), py::arg("eCase"));

        cls.def("getIndex", &StringC::getIndex);
        cls.def("setIndex", &StringC::setIndex, "", py::arg("newIndex"));

        cls.def("getName", &StringC::getName);
        cls.def("setName", &StringC::setName, "", py::arg("newName"));

        cls.def("getDouble", &StringC::getDouble);
        cls.def("setDouble", &StringC::setDouble, "", py::arg("dVal"));

        cls.def("setCaseI", &StringC::setCaseI, "", py::arg("eCase"));
        cls.def("getCaseI", &StringC::getCaseI);
        cls.def("setCaseG", &StringC::setCaseG, "", py::arg("eCase"));
        cls.def("getCaseG", &StringC::getCaseG);


        cls.def("methodCombine1", (std::string (StringC::*)(const std::string&, const std::string&)) &StringC::methodCombine1,"Combine strings return item", py::arg("categoryName"), py::arg("attribName"));

        cls.def("methodCombine2", [](StringC &o, std::string &cifItem, std::string categoryName, std::string itemName) {
            o.methodCombine2(cifItem, categoryName, itemName);
            return std::make_tuple(cifItem, categoryName, itemName);
            }, "", py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName") );

        cls.def("methodCombine2", [](StringC &o, std::string &cifItem, std::string categoryName, std::string itemName) {
            o.methodCombine2(cifItem, categoryName, itemName);
            return std::make_tuple(cifItem, categoryName, itemName);
            }, "", py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName") );

        cls.def("methodCombine2", [](StringC &o, std::string &cifItem, std::string categoryName, std::string itemName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR) {
            o.methodCombine2(cifItem, categoryName, itemName, PREFIX_CHAR, JOIN_CHAR);
            return std::make_tuple(cifItem, categoryName, itemName);
            }, "", py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName"), py::arg("PREFIX_CHAR"), py::arg("JOIN_CHAR")   );

        cls.def("methodCombine3", [](StringC &o, std::vector<std::string>& cifItems, std::string categoryName, std::vector<std::string> attribsNames) {
            o.methodCombine3(cifItems, categoryName, attribsNames);
            return std::make_tuple(cifItems, categoryName, attribsNames);
            }, "", py::arg("cifItems"), py::arg("categoryName"), py::arg("attribsNames") );

        cls.def("methodSetAndReturn4", &StringC::methodSetAndReturn4,"Combine strings return list", py::arg("categoryName"), py::arg("attribsNames") );


        //cls.def("IsEmptyValue", &StringC::IsEmptyValue);
        cls.def("IsEmptyValue", (bool (StringC::*)(const std::string&)) &StringC::IsEmptyValue, "C++: StringC::IsEmptyValue(const std::string&) --> bool", py::arg("value"));

        //cls.def("IsSpecialChar", &StringC::IsSpecialChar);
        cls.def_static("IsSpecialChar", (bool (*)(const char)) &StringC::IsSpecialChar, "C++: StringC::IsSpecialChar(const char) --> bool", py::arg("charValue"));

}
