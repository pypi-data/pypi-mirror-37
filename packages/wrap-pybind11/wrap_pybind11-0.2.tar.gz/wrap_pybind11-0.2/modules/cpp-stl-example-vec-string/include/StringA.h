
//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


#ifndef STRINGA_H
#define STRINGA_H


#include <string>
#include <vector>

enum eCompareType
    {
        eCASE_SENSITIVE = 0,
        eCASE_INSENSITIVE,
        eWS_INSENSITIVE,  // But case-sensitive
        eAS_INTEGER
    };

/**
 ** \class StringA
 **
 ** \brief Example class to provide Python binding test cases for string types and vectors of strings.
 **
 */
class StringA
{
public:

    enum eCompareTypeC
    {
        eCASE_SENSITIVE = 0,
        eCASE_INSENSITIVE,
        eWS_INSENSITIVE,  // But case-sensitive
        eAS_INTEGER
    };

private:
    std::string myName;
    int myIndex;
    double myDouble;
    std::vector<std::string> myStringVec;
    eCompareTypeC caseSettingI;
    eCompareType  caseSettingG;
public:

    static const char PREFIX_CHAR = '_';
    static const char JOIN_CHAR = '.';
    static const char NULL_CHAR = '?';
    static const char NOT_APPROPRIATE_CHAR = '.';
    static const std::string UnknownValue;
    static const std::string InapplicableValue;
    //
    // Overloaded constructors -
    //
    StringA();
    StringA(int index);
    StringA(double dVal);
    StringA(const std::string& name);
    StringA(const std::string& name, const eCompareTypeC eCase );

    ~StringA();
    void setCaseI(const eCompareTypeC eCase);
    void setCaseG(const eCompareType  eCase);
    eCompareTypeC getCaseI();
    eCompareType  getCaseG();
    //

    int getIndex();
    void setIndex(const int newIndex);

    double getDouble();
    void setDouble(const double dVal);

    std::string& getName();

    void setName(std::string newName);

    std::string methodCombine1(const std::string& categoryName, const std::string& attribName);

    void methodCombine2(std::string& cifItem,  const std::string& categoryName, const std::string& attribName);

    void methodCombine3(std::vector<std::string>& cifItems, const std::string& categoryName, const std::vector<std::string>& attribsNames);

    const std::vector<std::string>& methodSetAndReturn4(const std::string& categoryName, const std::vector<std::string>& attribsNames);

    bool IsEmptyValue(const std::string& value);

    static bool IsSpecialChar(const char charValue);

};

inline StringA::StringA()
{
    myIndex = 0;
    myName = "";
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = StringA::eCompareTypeC::eCASE_INSENSITIVE;
}

inline StringA::StringA(double dval)
{
    myIndex = 0;
    myName = "";
    myDouble = dval;
    myStringVec.clear();
    caseSettingI = StringA::eCompareTypeC::eCASE_INSENSITIVE;
}

inline  StringA::StringA(int index)
{
    myIndex = index;
    myName = "";
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = StringA::eCompareTypeC::eCASE_INSENSITIVE;
}

inline StringA::StringA(const std::string& name )
{
    myIndex = 0;
    myName = name;
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = StringA::eCompareTypeC::eCASE_INSENSITIVE;
}

inline StringA::StringA(const std::string& name, const eCompareTypeC eCase )
{
    myIndex = 0;
    myName = name;
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = eCase;
}

inline StringA::~StringA()
{
    myStringVec.clear();
}

inline void StringA::setCaseI(const eCompareTypeC eCase)
{

   caseSettingI = eCase;

}

inline void StringA::setCaseG(const eCompareType eCase)
{

   caseSettingG = eCase;

}

inline StringA::eCompareTypeC StringA::getCaseI()
{
    return(caseSettingI);
}

inline  eCompareType StringA::getCaseG()
{
    return(caseSettingG);
}

inline int StringA::getIndex()
{
    return(myIndex);
}

inline void StringA::setIndex(const int newIndex)
{

    myIndex = newIndex;

}

inline void StringA::setName(const std::string newName)
{

    myName = newName;

}

inline std::string& StringA::getName()
{

    return myName;
}

inline double StringA::getDouble()
{

    return(myDouble);

}

inline void StringA::setDouble(const double dVal)
{

    myDouble = dVal;

}


#endif
