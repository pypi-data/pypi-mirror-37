// File: ./wrapStringA.cpp
// Date: 2018-10-14
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <vector>
#include "StringA.h"
namespace py = pybind11;
using namespace pybind11::literals;

void wrapStringA(py::module &m) {
   m.doc() = "Wrapper for header file StringA.h";

   py::enum_<eCompareType>(m, "eCompareType")
     .value("eCASE_SENSITIVE", eCompareType::eCASE_SENSITIVE)
     .value("eCASE_INSENSITIVE", eCompareType::eCASE_INSENSITIVE)
     .value("eWS_INSENSITIVE", eCompareType::eWS_INSENSITIVE)
     .value("eAS_INTEGER", eCompareType::eAS_INTEGER);

   {
    py::class_<StringA, std::shared_ptr<StringA>> cls(m, "StringA", "Wrapper for class StringA");
   
      py::enum_<StringA::eCompareTypeC>(cls, "eCompareTypeC")
        .value("eCASE_SENSITIVE", StringA::eCompareTypeC::eCASE_SENSITIVE)
        .value("eCASE_INSENSITIVE", StringA::eCompareTypeC::eCASE_INSENSITIVE)
        .value("eWS_INSENSITIVE", StringA::eCompareTypeC::eWS_INSENSITIVE)
        .value("eAS_INTEGER", StringA::eCompareTypeC::eAS_INTEGER);
   
     cls.def(py::init<>());
     cls.def(py::init<int>(),py::arg("index"));
     cls.def(py::init<double>(),py::arg("dVal"));
     cls.def(py::init<const std::string &>(),py::arg("name"));
     cls.def(py::init<const std::string &,const StringA::eCompareTypeC>(),py::arg("name"),py::arg("eCase"));
     cls.def("setCaseI", &StringA::setCaseI,"",py::arg("eCase"));
     cls.def("setCaseG", &StringA::setCaseG,"",py::arg("eCase"));
     cls.def("getCaseI", &StringA::getCaseI,"");
     cls.def("getCaseG", &StringA::getCaseG,"");
     cls.def("getIndex", &StringA::getIndex,"");
     cls.def("setIndex", &StringA::setIndex,"",py::arg("newIndex"));
     cls.def("getDouble", &StringA::getDouble,"");
     cls.def("setDouble", &StringA::setDouble,"",py::arg("dVal"));
     cls.def("getName", &StringA::getName,"");
     cls.def("setName", &StringA::setName,"",py::arg("newName"));
     cls.def("methodCombine1", &StringA::methodCombine1,"",py::arg("categoryName"), py::arg("attribName"));
     cls.def("methodCombine2", [](StringA &o , std::string & cifItem, const std::string & categoryName, const std::string & attribName) {
        o.methodCombine2(cifItem, categoryName, attribName);
       return cifItem;
     },"methodCombine2 with arguments cifItem, categoryName, attribName" , py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName"));
     cls.def("methodCombine3", [](StringA &o , std::vector<std::string> & cifItems, const std::string & categoryName, const std::vector<std::string> & attribsNames) {
        o.methodCombine3(cifItems, categoryName, attribsNames);
       return cifItems;
     },"methodCombine3 with arguments cifItems, categoryName, attribsNames" , py::arg("cifItems"), py::arg("categoryName"), py::arg("attribsNames"));
     cls.def("methodSetAndReturn4", &StringA::methodSetAndReturn4,"",py::arg("categoryName"), py::arg("attribsNames"));
     cls.def("IsEmptyValue", (bool (StringA::*)(const std::string &)) &StringA::IsEmptyValue,"IsEmptyValue with arguments const std::string &",py::arg("value"));
     cls.def_static("IsSpecialChar", (bool (*)(const char)) &StringA::IsSpecialChar,"IsSpecialChar with arguments const char",py::arg("charValue"));
   }

}