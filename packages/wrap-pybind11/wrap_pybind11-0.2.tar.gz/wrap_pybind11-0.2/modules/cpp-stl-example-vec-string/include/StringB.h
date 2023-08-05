
//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


#ifndef STRINGB_H
#define STRINGB_H


#include <string>
#include <vector>

enum eCompareTypeP
    {
        eCASE_SENSITIVE = 0,
        eCASE_INSENSITIVE,
        eWS_INSENSITIVE,  // But case-sensitive
        eAS_INTEGER
    };

/**
 ** \class StringB
 **
 ** \brief Example class to provide Python binding test cases for string types and vectors of strings w/overloaded methods -
 **
 */
class StringB
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
    eCompareTypeP  caseSettingG;
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
    StringB();
    StringB(int index);
    StringB(double dVal);
    StringB(const std::string& name);
    StringB(const std::string& name, const eCompareTypeC eCase );

    ~StringB();
    void setCaseI(const eCompareTypeC eCase);
    void setCaseG(const eCompareTypeP  eCase);
    eCompareTypeC getCaseI();
    eCompareTypeP getCaseG();
    //

    int getIndex();
    void setIndex(const int newIndex);

    double getDouble();
    void setDouble(const double dVal);

    std::string& getName();

    void setName(std::string newName);

    //
    //
    void setStuff(int newIndex);
    void setStuff(double dVal);
    void setStuff(int newIndex, double dVal);
    void setStuff(int newIndex, double dVal, const eCompareTypeC eCase );

    std::string methodCombine1(const std::string& categoryName, const std::string& attribName);
    std::string methodCombine1(const std::string& categoryName, const std::string& attribName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR);

    void methodCombine2(std::string& cifItem,  const std::string& categoryName, const std::string& attribName);
    void methodCombine2(std::string& cifItem,  const std::string& categoryName, const std::string& attribName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR);

    void methodCombine3(std::vector<std::string>& cifItems, const std::string& categoryName, const std::vector<std::string>& attribsNames);

    const std::vector<std::string>& methodSetAndReturn4(const std::string& categoryName, const std::vector<std::string>& attribsNames);

    bool IsEmptyValue(const std::string& value);

    static bool IsSpecialChar(const char charValue);

};

inline StringB::StringB()
{
    myIndex = 0;
    myName = "";
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = StringB::eCompareTypeC::eCASE_INSENSITIVE;
}

inline StringB::StringB(double dval)
{
    myIndex = 0;
    myName = "";
    myDouble = dval;
    myStringVec.clear();
    caseSettingI = StringB::eCompareTypeC::eCASE_INSENSITIVE;
}

inline  StringB::StringB(int index)
{
    myIndex = index;
    myName = "";
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = StringB::eCompareTypeC::eCASE_INSENSITIVE;
}

inline StringB::StringB(const std::string& name )
{
    myIndex = 0;
    myName = name;
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = StringB::eCompareTypeC::eCASE_INSENSITIVE;
}

inline StringB::StringB(const std::string& name, const eCompareTypeC eCase )
{
    myIndex = 0;
    myName = name;
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = eCase;
}

inline StringB::~StringB()
{
    myStringVec.clear();
}

inline void StringB::setStuff(int newIndex)
{
   myIndex = newIndex;
}

inline void StringB::setStuff(double dVal)
{
   myDouble = dVal;
}

inline void StringB::setStuff(int newIndex, double dVal)
{
   myIndex = newIndex;
   myDouble = dVal;
}


inline void StringB::setStuff(int newIndex, double dVal, const eCompareTypeC eCase)
{
   myIndex = newIndex;
   myDouble = dVal;
   caseSettingI = eCase;

}




inline void StringB::setCaseI(const eCompareTypeC eCase)
{

   caseSettingI = eCase;

}

inline void StringB::setCaseG(const eCompareTypeP eCase)
{

   caseSettingG = eCase;

}

inline StringB::eCompareTypeC StringB::getCaseI()
{
    return(caseSettingI);
}

inline  eCompareTypeP StringB::getCaseG()
{
    return(caseSettingG);
}

inline int StringB::getIndex()
{
    return(myIndex);
}

inline void StringB::setIndex(const int newIndex)
{

    myIndex = newIndex;

}

inline void StringB::setName(const std::string newName)
{

    myName = newName;

}

inline std::string& StringB::getName()
{

    return myName;
}

inline double StringB::getDouble()
{

    return(myDouble);

}

inline void StringB::setDouble(const double dVal)
{

    myDouble = dVal;

}


#endif
