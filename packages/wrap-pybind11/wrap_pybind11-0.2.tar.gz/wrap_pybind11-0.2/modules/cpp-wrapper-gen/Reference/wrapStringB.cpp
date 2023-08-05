#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <string>

#include "StringB.h"

namespace py = pybind11;
using namespace pybind11::literals;

//PYBIND11_MAKE_OPAQUE(std::vector<std::string>);

void wrapStringB(py::module &m) {
    m.doc() = "Wrapper test example for strings and vectors";

    py::class_<StringB> cls(m, "StringB", "STL String and Vector test cases");
        //py::handle cl_type = cls;
        py::enum_<StringB::eCompareTypeC>(cls,"eCompareTypeC")
            .value("eCASE_SENSITIVE", StringB::eCompareTypeC::eCASE_SENSITIVE)
            .value("eCASE_INSENSITIVE", StringB::eCompareTypeC::eCASE_INSENSITIVE)
            .value("eWS_INSENSITIVE", StringB::eCompareTypeC::eWS_INSENSITIVE)
            .value("eAS_INTEGER", StringB::eCompareTypeC::eAS_INTEGER)
            .export_values();
        cls.def(py::init<>());
        cls.def(py::init<double>(), py::arg("dVal"));
        cls.def(py::init<int>(), py::arg("dVal"));
        cls.def(py::init<std::string>(), py::arg("name"));
        cls.def(py::init<std::string, StringB::eCompareTypeC>(), py::arg("name"), py::arg("eCase"));
        // overloaded examples -
        cls.def("setStuff", (void (StringB::*)(int)) &StringB::setStuff, "Setstuff int", py::arg("newIndex"));
        cls.def("setStuff", (void (StringB::*)(double)) &StringB::setStuff, "Setstuff double", py::arg("dVal"));
        cls.def("setStuff", (void (StringB::*)(int, double)) &StringB::setStuff, "Setstuff int and double", py::arg("newIndex"), py::arg("dVal"));
        cls.def("setStuff", (void (StringB::*)(int, double, const StringB::eCompareTypeC )) &StringB::setStuff, "Setstuff int and double,enum", py::arg("newIndex"), py::arg("dVal"), py::arg("eCase"));

        cls.def("getIndex", &StringB::getIndex);
        cls.def("setIndex", &StringB::setIndex, "", py::arg("newIndex"));

        cls.def("getName", &StringB::getName);
        cls.def("setName", &StringB::setName, "", py::arg("newName"));

        cls.def("getDouble", &StringB::getDouble);
        cls.def("setDouble", &StringB::setDouble, "", py::arg("dVal"));

        cls.def("setCaseI", &StringB::setCaseI, "", py::arg("eCase"));
        cls.def("getCaseI", &StringB::getCaseI);
        cls.def("setCaseG", &StringB::setCaseG, "", py::arg("eCase"));
        cls.def("getCaseG", &StringB::getCaseG);


        cls.def("methodCombine1", (std::string (StringB::*)(const std::string&, const std::string&)) &StringB::methodCombine1,"Combine strings return item", py::arg("categoryName"), py::arg("attribName"));

        cls.def("methodCombine2", [](StringB &o, std::string &cifItem, std::string categoryName, std::string itemName) {
            o.methodCombine2(cifItem, categoryName, itemName);
            return std::make_tuple(cifItem, categoryName, itemName);
            }, "", py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName") );

        cls.def("methodCombine2", [](StringB &o, std::string &cifItem, std::string categoryName, std::string itemName) {
            o.methodCombine2(cifItem, categoryName, itemName);
            return std::make_tuple(cifItem, categoryName, itemName);
            }, "", py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName") );

        cls.def("methodCombine2", [](StringB &o, std::string &cifItem, std::string categoryName, std::string itemName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR) {
            o.methodCombine2(cifItem, categoryName, itemName, PREFIX_CHAR, JOIN_CHAR);
            return std::make_tuple(cifItem, categoryName, itemName);
            }, "", py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName"), py::arg("PREFIX_CHAR"), py::arg("JOIN_CHAR")   );

        cls.def("methodCombine3", [](StringB &o, std::vector<std::string>& cifItems, std::string categoryName, std::vector<std::string> attribsNames) {
            o.methodCombine3(cifItems, categoryName, attribsNames);
            return std::make_tuple(cifItems, categoryName, attribsNames);
            }, "", py::arg("cifItems"), py::arg("categoryName"), py::arg("attribsNames") );

        cls.def("methodSetAndReturn4", &StringB::methodSetAndReturn4,"Combine strings return list", py::arg("categoryName"), py::arg("attribsNames") );


        //cls.def("IsEmptyValue", &StringB::IsEmptyValue);
        cls.def("IsEmptyValue", (bool (StringB::*)(const std::string&)) &StringB::IsEmptyValue, "C++: StringB::IsEmptyValue(const std::string&) --> bool", py::arg("value"));

        //cls.def("IsSpecialChar", &StringB::IsSpecialChar);
        cls.def_static("IsSpecialChar", (bool (*)(const char)) &StringB::IsSpecialChar, "C++: StringB::IsSpecialChar(const char) --> bool", py::arg("charValue"));

}
