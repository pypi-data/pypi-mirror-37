// File: ./wrapStringC.cpp
// Date: 2018-10-14
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <vector>
#include "StringC.h"
namespace py = pybind11;
using namespace pybind11::literals;

void wrapStringC(py::module &m) {
   m.doc() = "Wrapper for header file StringC.h";

   py::enum_<eCompareTypeG>(m, "eCompareTypeG")
     .value("eCASE_SENSITIVE", eCompareTypeG::eCASE_SENSITIVE)
     .value("eCASE_INSENSITIVE", eCompareTypeG::eCASE_INSENSITIVE)
     .value("eWS_INSENSITIVE", eCompareTypeG::eWS_INSENSITIVE)
     .value("eAS_INTEGER", eCompareTypeG::eAS_INTEGER);

     m.def("setStuffG", (void (*)(int )) &setStuffG, "setStuffG with arguments int ", py::arg("newIndex"));
     m.def("setStuffG", (void (*)(double )) &setStuffG, "setStuffG with arguments double ", py::arg("dVal"));
     m.def("setStuffG", (void (*)(int , double )) &setStuffG, "setStuffG with arguments int , double ", py::arg("newIndex"), py::arg("dVal"));
     m.def("setStuffG", (void (*)(int , double , const eCompareTypeG )) &setStuffG, "setStuffG with arguments int , double , const eCompareTypeG ", py::arg("newIndex"), py::arg("dVal"), py::arg("eCase"));
     m.def("setStuffG", (void (*)(int )) &setStuffG, "setStuffG with arguments int ", py::arg("newIndex"));
     m.def("setStuffG", (void (*)(double )) &setStuffG, "setStuffG with arguments double ", py::arg("dVal"));
     m.def("setStuffG", (void (*)(int , double )) &setStuffG, "setStuffG with arguments int , double ", py::arg("newIndex"), py::arg("dVal"));
     m.def("setStuffG", (void (*)(int , double , const eCompareTypeG )) &setStuffG, "setStuffG with arguments int , double , const eCompareTypeG ", py::arg("newIndex"), py::arg("dVal"), py::arg("eCase"));
     m.def("methodCombine1G", (std::string (*)(const std::string &, const std::string &)) &methodCombine1G, "methodCombine1G with arguments const std::string &, const std::string &", py::arg("categoryName"), py::arg("attribName"));
     m.def("methodCombine1G", (std::string (*)(const std::string &, const std::string &, const std::string &, const std::string &)) &methodCombine1G, "methodCombine1G with arguments const std::string &, const std::string &, const std::string &, const std::string &", py::arg("categoryName"), py::arg("attribName"), py::arg("PREFIX_CHAR"), py::arg("JOIN_CHAR"));
     m.def("methodCombine2G", [](std::string &cifItem, const std::string &categoryName, const std::string &attribName) {
        methodCombine2G(cifItem, categoryName, attribName);
       return cifItem;
     },"methodCombine2G with arguments cifItem, categoryName, attribName", py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName"));
     m.def("methodCombine2G", [](std::string &cifItem, const std::string &categoryName, const std::string &attribName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR) {
        methodCombine2G(cifItem, categoryName, attribName, PREFIX_CHAR, JOIN_CHAR);
       return cifItem;
     },"methodCombine2G with arguments cifItem, categoryName, attribName, PREFIX_CHAR, JOIN_CHAR", py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName"), py::arg("PREFIX_CHAR"), py::arg("JOIN_CHAR"));
     m.def("methodCombine3G", [](std::vector<std::string> &cifItems, const std::string &categoryName, const std::vector<std::string> &attribsNames) {
        methodCombine3G(cifItems, categoryName, attribsNames);
       return cifItems;
     },"methodCombine3G with arguments cifItems, categoryName, attribsNames", py::arg("cifItems"), py::arg("categoryName"), py::arg("attribsNames"));
   {
    py::class_<StringC, std::shared_ptr<StringC>> cls(m, "StringC", "Wrapper for class StringC");
   
      py::enum_<StringC::eCompareTypeC>(cls, "eCompareTypeC")
        .value("eCASE_SENSITIVE", StringC::eCompareTypeC::eCASE_SENSITIVE)
        .value("eCASE_INSENSITIVE", StringC::eCompareTypeC::eCASE_INSENSITIVE)
        .value("eWS_INSENSITIVE", StringC::eCompareTypeC::eWS_INSENSITIVE)
        .value("eAS_INTEGER", StringC::eCompareTypeC::eAS_INTEGER);
   
     cls.def(py::init<>());
     cls.def(py::init<int>(),py::arg("index"));
     cls.def(py::init<double>(),py::arg("dVal"));
     cls.def(py::init<const std::string &>(),py::arg("name"));
     cls.def(py::init<const std::string &,const StringC::eCompareTypeC>(),py::arg("name"),py::arg("eCase"));
     cls.def("setCaseI", &StringC::setCaseI,"",py::arg("eCase"));
     cls.def("setCaseG", &StringC::setCaseG,"",py::arg("eCase"));
     cls.def("getCaseI", &StringC::getCaseI,"");
     cls.def("getCaseG", &StringC::getCaseG,"");
     cls.def("getIndex", &StringC::getIndex,"");
     cls.def("setIndex", &StringC::setIndex,"",py::arg("newIndex"));
     cls.def("getDouble", &StringC::getDouble,"");
     cls.def("setDouble", &StringC::setDouble,"",py::arg("dVal"));
     cls.def("getName", &StringC::getName,"");
     cls.def("setName", &StringC::setName,"",py::arg("newName"));
     cls.def("setStuff", (void (StringC::*)(int)) &StringC::setStuff,"setStuff with arguments int",py::arg("newIndex"));
     cls.def("setStuff", (void (StringC::*)(double)) &StringC::setStuff,"setStuff with arguments double",py::arg("dVal"));
     cls.def("setStuff", (void (StringC::*)(int, double)) &StringC::setStuff,"setStuff with arguments int, double",py::arg("newIndex"), py::arg("dVal"));
     cls.def("setStuff", (void (StringC::*)(int, double, const StringC::eCompareTypeC)) &StringC::setStuff,"setStuff with arguments int, double, const StringC::eCompareTypeC",py::arg("newIndex"), py::arg("dVal"), py::arg("eCase"));
     cls.def("methodCombine1", (std::string (StringC::*)(const std::string &, const std::string &)) &StringC::methodCombine1,"methodCombine1 with arguments const std::string &, const std::string &",py::arg("categoryName"), py::arg("attribName"));
     cls.def("methodCombine1", (std::string (StringC::*)(const std::string &, const std::string &, const std::string &, const std::string &)) &StringC::methodCombine1,"methodCombine1 with arguments const std::string &, const std::string &, const std::string &, const std::string &",py::arg("categoryName"), py::arg("attribName"), py::arg("PREFIX_CHAR"), py::arg("JOIN_CHAR"));
     cls.def("methodCombine2", [](StringC &o , std::string & cifItem, const std::string & categoryName, const std::string & attribName) {
        o.methodCombine2(cifItem, categoryName, attribName);
       return cifItem;
     },"methodCombine2 with arguments cifItem, categoryName, attribName" , py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName"));
     cls.def("methodCombine2", [](StringC &o , std::string & cifItem, const std::string & categoryName, const std::string & attribName, const std::string & PREFIX_CHAR, const std::string & JOIN_CHAR) {
        o.methodCombine2(cifItem, categoryName, attribName, PREFIX_CHAR, JOIN_CHAR);
       return cifItem;
     },"methodCombine2 with arguments cifItem, categoryName, attribName, PREFIX_CHAR, JOIN_CHAR" , py::arg("cifItem"), py::arg("categoryName"), py::arg("attribName"), py::arg("PREFIX_CHAR"), py::arg("JOIN_CHAR"));
     cls.def("methodCombine3", [](StringC &o , std::vector<std::string> & cifItems, const std::string & categoryName, const std::vector<std::string> & attribsNames) {
        o.methodCombine3(cifItems, categoryName, attribsNames);
       return cifItems;
     },"methodCombine3 with arguments cifItems, categoryName, attribsNames" , py::arg("cifItems"), py::arg("categoryName"), py::arg("attribsNames"));
     cls.def("methodSetAndReturn4", &StringC::methodSetAndReturn4,"",py::arg("categoryName"), py::arg("attribsNames"));
     cls.def("IsEmptyValue", (bool (StringC::*)(const std::string &)) &StringC::IsEmptyValue,"IsEmptyValue with arguments const std::string &",py::arg("value"));
     cls.def_static("IsSpecialChar", (bool (*)(const char)) &StringC::IsSpecialChar,"IsSpecialChar with arguments const char",py::arg("charValue"));
   }

}