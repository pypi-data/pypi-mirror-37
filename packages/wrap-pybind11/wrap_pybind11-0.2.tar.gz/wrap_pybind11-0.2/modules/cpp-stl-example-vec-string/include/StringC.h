
//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


#ifndef STRINGC_H
#define STRINGC_H


#include <string>
#include <vector>

enum eCompareTypeG
    {
        eCASE_SENSITIVE = 0,
        eCASE_INSENSITIVE,
        eWS_INSENSITIVE,  // But case-sensitive
        eAS_INTEGER
    };


// Global functions  -
void setStuffG(int newIndex);
void setStuffG(double dVal);
void setStuffG(int newIndex, double dVal);
void setStuffG(int newIndex, double dVal, const eCompareTypeG eCase );

std::string methodCombine1G(const std::string& categoryName, const std::string& attribName);
std::string methodCombine1G(const std::string& categoryName, const std::string& attribName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR);

void methodCombine2G(std::string& cifItem,  const std::string& categoryName, const std::string& attribName);
void methodCombine2G(std::string& cifItem,  const std::string& categoryName, const std::string& attribName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR);
void methodCombine3G(std::vector<std::string>& cifItems, const std::string& categoryName, const std::vector<std::string>& attribsNames);

/**
 ** \class StringC
 **
 ** \brief Example class to provide Python binding test cases for string types and vectors of strings w/overloaded methods -
 **
 */
class StringC
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
    eCompareTypeG  caseSettingG;
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
    StringC();
    StringC(int index);
    StringC(double dVal);
    StringC(const std::string& name);
    StringC(const std::string& name, const eCompareTypeC eCase );

    ~StringC();
    void setCaseI(const eCompareTypeC eCase);
    void setCaseG(const eCompareTypeG  eCase);
    eCompareTypeC getCaseI();
    eCompareTypeG  getCaseG();
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

inline StringC::StringC()
{
    myIndex = 0;
    myName = "";
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = StringC::eCompareTypeC::eCASE_INSENSITIVE;
}

inline StringC::StringC(double dval)
{
    myIndex = 0;
    myName = "";
    myDouble = dval;
    myStringVec.clear();
    caseSettingI = StringC::eCompareTypeC::eCASE_INSENSITIVE;
}

inline  StringC::StringC(int index)
{
    myIndex = index;
    myName = "";
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = StringC::eCompareTypeC::eCASE_INSENSITIVE;
}

inline StringC::StringC(const std::string& name )
{
    myIndex = 0;
    myName = name;
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = StringC::eCompareTypeC::eCASE_INSENSITIVE;
}

inline StringC::StringC(const std::string& name, const eCompareTypeC eCase )
{
    myIndex = 0;
    myName = name;
    myDouble = 0.0;
    myStringVec.clear();
    caseSettingI = eCase;
}

inline StringC::~StringC()
{
    myStringVec.clear();
}

inline void StringC::setStuff(int newIndex)
{
   myIndex = newIndex;
}

inline void StringC::setStuff(double dVal)
{
   myDouble = dVal;
}

inline void StringC::setStuff(int newIndex, double dVal)
{
   myIndex = newIndex;
   myDouble = dVal;
}


inline void StringC::setStuff(int newIndex, double dVal, const eCompareTypeC eCase)
{
   myIndex = newIndex;
   myDouble = dVal;
   caseSettingI = eCase;

}




inline void StringC::setCaseI(const eCompareTypeC eCase)
{

   caseSettingI = eCase;

}

inline void StringC::setCaseG(const eCompareTypeG eCase)
{

   caseSettingG = eCase;

}

inline StringC::eCompareTypeC StringC::getCaseI()
{
    return(caseSettingI);
}

inline  eCompareTypeG StringC::getCaseG()
{
    return(caseSettingG);
}

inline int StringC::getIndex()
{
    return(myIndex);
}

inline void StringC::setIndex(const int newIndex)
{

    myIndex = newIndex;

}

inline void StringC::setName(const std::string newName)
{

    myName = newName;

}

inline std::string& StringC::getName()
{

    return myName;
}

inline double StringC::getDouble()
{

    return(myDouble);

}

inline void StringC::setDouble(const double dVal)
{

    myDouble = dVal;

}

//

inline void setStuffG(int newIndex)
{
   int myIndex = newIndex;
}

inline void setStuffG(double dVal)
{
   double myDouble = dVal;
}

inline void setStuffG(int newIndex, double dVal)
{
   int myIndex = newIndex;
   double myDouble = dVal;
}


inline void setStuffG(int newIndex, double dVal, const eCompareTypeG eCase)
{
   int myIndex = newIndex;
   double myDouble = dVal;
   eCompareTypeG caseSettingI = eCase;

}


#endif
