#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <string>

#include "StringA.h"

namespace py = pybind11;
using namespace pybind11::literals;

//PYBIND11_MAKE_OPAQUE(std::vector<std::string>);

void wrapStringA(py::module &m) {
    m.doc() = "Wrapper test example for strings and vectors";

    py::enum_<eCompareType>(m, "eCompareType")
      .value("eCASE_SENSITIVE", eCompareType::eCASE_SENSITIVE)
      .value("eCASE_INSENSITIVE", eCompareType::eCASE_INSENSITIVE)
      .value("eWS_INSENSITIVE", eCompareType::eWS_INSENSITIVE)
      .value("eAS_INTEGER", eCompareType::eAS_INTEGER)
      .export_values();

    py::class_<StringA> cls(m, "StringA", "STL String and Vector test cases");
        //py::handle cl_type = cls;
        py::enum_<StringA::eCompareTypeC>(cls,"eCompareTypeC")
            .value("eCASE_SENSITIVE", StringA::eCompareTypeC::eCASE_SENSITIVE)
            .value("eCASE_INSENSITIVE", StringA::eCompareTypeC::eCASE_INSENSITIVE)
            .value("eWS_INSENSITIVE", StringA::eCompareTypeC::eWS_INSENSITIVE)
            .value("eAS_INTEGER", StringA::eCompareTypeC::eAS_INTEGER)
            .export_values();
        cls.def(py::init<>());
        cls.def(py::init<double>());
        cls.def(py::init<int>());
        cls.def(py::init<std::string>());
        cls.def(py::init<std::string, StringA::eCompareTypeC>());
        //
        cls.def("getIndex", &StringA::getIndex);
        cls.def("setIndex", &StringA::setIndex);

        cls.def("getName", &StringA::getName);
        cls.def("setName", &StringA::setName);

        cls.def("getDouble", &StringA::getDouble);
        cls.def("setDouble", &StringA::setDouble);

        cls.def("setCaseI", &StringA::setCaseI);
        cls.def("getCaseI", &StringA::getCaseI);
        cls.def("setCaseG", &StringA::setCaseG);
        cls.def("getCaseG", &StringA::getCaseG);

        cls.def("methodCombine1", &StringA::methodCombine1,"Combine strings return item", py::arg("categoryName"), py::arg("attribName"));

        cls.def("methodCombine2", [](StringA &o, std::string &cifItem, std::string categoryName, std::string itemName) {
            o.methodCombine2(cifItem, categoryName, itemName);
            return std::make_tuple(cifItem, categoryName, itemName);
            }, "", py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName") );

        cls.def("methodCombine3", [](StringA &o, std::vector<std::string>& cifItems, std::string categoryName, std::vector<std::string> attribsNames) {
            o.methodCombine3(cifItems, categoryName, attribsNames);
            return std::make_tuple(cifItems, categoryName, attribsNames);
            }, "", py::arg("cifItems"), py::arg("categoryName"), py::arg("attribsNames") );

        cls.def("methodSetAndReturn4", &StringA::methodSetAndReturn4,"Combine strings return list", py::arg("categoryName"), py::arg("attribsNames") );


        //cls.def("IsEmptyValue", &StringA::IsEmptyValue);
        cls.def("IsEmptyValue", (bool (StringA::*)(const std::string&)) &StringA::IsEmptyValue, "C++: StringA::IsEmptyValue(const std::string&) --> bool", py::arg("value"));

        //cls.def("IsSpecialChar", &StringA::IsSpecialChar);
        cls.def_static("IsSpecialChar", (bool (*)(const char)) &StringA::IsSpecialChar, "C++: StringA::IsSpecialChar(const char) --> bool", py::arg("charValue"));

}
