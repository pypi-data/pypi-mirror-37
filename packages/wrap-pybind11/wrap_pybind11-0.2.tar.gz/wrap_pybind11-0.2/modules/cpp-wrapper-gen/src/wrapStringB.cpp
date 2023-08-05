// File: ./wrapStringB.cpp
// Date: 2018-10-14
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <vector>
#include "StringB.h"
namespace py = pybind11;
using namespace pybind11::literals;

void wrapStringB(py::module &m) {
   m.doc() = "Wrapper for header file StringB.h";

   py::enum_<eCompareTypeP>(m, "eCompareTypeP")
     .value("eCASE_SENSITIVE", eCompareTypeP::eCASE_SENSITIVE)
     .value("eCASE_INSENSITIVE", eCompareTypeP::eCASE_INSENSITIVE)
     .value("eWS_INSENSITIVE", eCompareTypeP::eWS_INSENSITIVE)
     .value("eAS_INTEGER", eCompareTypeP::eAS_INTEGER);

   {
    py::class_<StringB, std::shared_ptr<StringB>> cls(m, "StringB", "Wrapper for class StringB");
   
      py::enum_<StringB::eCompareTypeC>(cls, "eCompareTypeC")
        .value("eCASE_SENSITIVE", StringB::eCompareTypeC::eCASE_SENSITIVE)
        .value("eCASE_INSENSITIVE", StringB::eCompareTypeC::eCASE_INSENSITIVE)
        .value("eWS_INSENSITIVE", StringB::eCompareTypeC::eWS_INSENSITIVE)
        .value("eAS_INTEGER", StringB::eCompareTypeC::eAS_INTEGER);
   
     cls.def(py::init<>());
     cls.def(py::init<int>(),py::arg("index"));
     cls.def(py::init<double>(),py::arg("dVal"));
     cls.def(py::init<const std::string &>(),py::arg("name"));
     cls.def(py::init<const std::string &,const StringB::eCompareTypeC>(),py::arg("name"),py::arg("eCase"));
     cls.def("setCaseI", &StringB::setCaseI,"",py::arg("eCase"));
     cls.def("setCaseG", &StringB::setCaseG,"",py::arg("eCase"));
     cls.def("getCaseI", &StringB::getCaseI,"");
     cls.def("getCaseG", &StringB::getCaseG,"");
     cls.def("getIndex", &StringB::getIndex,"");
     cls.def("setIndex", &StringB::setIndex,"",py::arg("newIndex"));
     cls.def("getDouble", &StringB::getDouble,"");
     cls.def("setDouble", &StringB::setDouble,"",py::arg("dVal"));
     cls.def("getName", &StringB::getName,"");
     cls.def("setName", &StringB::setName,"",py::arg("newName"));
     cls.def("setStuff", (void (StringB::*)(int)) &StringB::setStuff,"setStuff with arguments int",py::arg("newIndex"));
     cls.def("setStuff", (void (StringB::*)(double)) &StringB::setStuff,"setStuff with arguments double",py::arg("dVal"));
     cls.def("setStuff", (void (StringB::*)(int, double)) &StringB::setStuff,"setStuff with arguments int, double",py::arg("newIndex"), py::arg("dVal"));
     cls.def("setStuff", (void (StringB::*)(int, double, const StringB::eCompareTypeC)) &StringB::setStuff,"setStuff with arguments int, double, const StringB::eCompareTypeC",py::arg("newIndex"), py::arg("dVal"), py::arg("eCase"));
     cls.def("methodCombine1", (std::string (StringB::*)(const std::string &, const std::string &)) &StringB::methodCombine1,"methodCombine1 with arguments const std::string &, const std::string &",py::arg("categoryName"), py::arg("attribName"));
     cls.def("methodCombine1", (std::string (StringB::*)(const std::string &, const std::string &, const std::string &, const std::string &)) &StringB::methodCombine1,"methodCombine1 with arguments const std::string &, const std::string &, const std::string &, const std::string &",py::arg("categoryName"), py::arg("attribName"), py::arg("PREFIX_CHAR"), py::arg("JOIN_CHAR"));
     cls.def("methodCombine2", [](StringB &o , std::string & cifItem, const std::string & categoryName, const std::string & attribName) {
        o.methodCombine2(cifItem, categoryName, attribName);
       return cifItem;
     },"methodCombine2 with arguments cifItem, categoryName, attribName" , py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName"));
     cls.def("methodCombine2", [](StringB &o , std::string & cifItem, const std::string & categoryName, const std::string & attribName, const std::string & PREFIX_CHAR, const std::string & JOIN_CHAR) {
        o.methodCombine2(cifItem, categoryName, attribName, PREFIX_CHAR, JOIN_CHAR);
       return cifItem;
     },"methodCombine2 with arguments cifItem, categoryName, attribName, PREFIX_CHAR, JOIN_CHAR" , py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName"), py::arg("PREFIX_CHAR"), py::arg("JOIN_CHAR"));
     cls.def("methodCombine3", [](StringB &o , std::vector<std::string> & cifItems, const std::string & categoryName, const std::vector<std::string> & attribsNames) {
        o.methodCombine3(cifItems, categoryName, attribsNames);
       return cifItems;
     },"methodCombine3 with arguments cifItems, categoryName, attribsNames" , py::arg("cifItems"), py::arg("categoryName"), py::arg("attribsNames"));
     cls.def("methodSetAndReturn4", &StringB::methodSetAndReturn4,"",py::arg("categoryName"), py::arg("attribsNames"));
     cls.def("IsEmptyValue", (bool (StringB::*)(const std::string &)) &StringB::IsEmptyValue,"IsEmptyValue with arguments const std::string &",py::arg("value"));
     cls.def_static("IsSpecialChar", (bool (*)(const char)) &StringB::IsSpecialChar,"IsSpecialChar with arguments const char",py::arg("charValue"));
   }

}