//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$

#include <string>
#include <vector>

#include "Exceptions.h"
#include "StringC.h"


using std::string;
using std::vector;



const std::string StringC::UnknownValue("?");
const std::string StringC::InapplicableValue(".");

std::string methodCombine1G(const std::string& categoryName,  const std::string& attribName)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "methodcombine1G");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name","methodcombine1G");
    }

    std::string cifItem = '_' + categoryName + '.' + attribName;
    return cifItem;
}

std::string methodCombine1G(const std::string& categoryName,  const std::string& attribName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "methodCombine1G");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name", "methodCombine1G");
    }

    std::string cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
    return cifItem;
}

// Update argument passed as reference with result -
void methodCombine2G(std::string& cifItem, const std::string& categoryName,  const std::string& attribName)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "methodcombine2G");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name",  "methodcombine2G");
    }

    cifItem = '_' + categoryName + '.' + attribName;
}

void methodCombine2G(std::string& cifItem, const std::string& categoryName,  const std::string& attribName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "methodcombine2G");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name",  "methodcombine2G");
    }

    cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
}

void methodCombine3G(std::vector<std::string>& cifItems, const std::string& categoryName, const std::vector<std::string>& attribsNames)
{
    cifItems.assign(attribsNames.size(), std::string());

    for (unsigned int attribI = 0; attribI < attribsNames.size(); ++attribI)
    {
        methodCombine2G(cifItems[attribI], categoryName, attribsNames[attribI]);
    }
}


// Return by value
//

std::string StringC::methodCombine1(const string& categoryName,  const string& attribName)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "StringC::MakeCifItem");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name","StringC::MakeCifItem");
    }

    std::string cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
    return cifItem;
}

std::string StringC::methodCombine1(const string& categoryName,  const string& attribName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "StringC::MakeCifItem");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name","StringC::MakeCifItem");
    }

    std::string cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
    return cifItem;
}


// Update argument passed as reference with result -
void StringC::methodCombine2(string& cifItem, const string& categoryName,  const string& attribName)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "StringC::MakeCifItem");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name",  "StringC::MakeCifItem");
    }

    cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
}

void StringC::methodCombine2(string& cifItem, const string& categoryName,  const string& attribName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "StringC::MakeCifItem");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name",  "StringC::MakeCifItem");
    }

    cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
}


void StringC::methodCombine3(std::vector<std::string>& cifItems, const std::string& categoryName, const std::vector<std::string>& attribsNames)
{
    cifItems.assign(attribsNames.size(), string());

    for (unsigned int attribI = 0; attribI < attribsNames.size(); ++attribI)
    {
        methodCombine2(cifItems[attribI], categoryName, attribsNames[attribI]);
    }
}


const std::vector<std::string>& StringC::methodSetAndReturn4(const std::string& categoryName, const std::vector<std::string>& attribsNames)
{
    myStringVec.clear();
    myStringVec.assign(attribsNames.size(), string());

    for (unsigned int attribI = 0; attribI < attribsNames.size(); ++attribI)
    {
        methodCombine2(myStringVec[attribI], categoryName, attribsNames[attribI]);
    }
    return myStringVec;
}



bool StringC::IsEmptyValue(const string& value)
{
    if (value.empty() || (value == InapplicableValue) ||
      (value == UnknownValue))
    {
        return (true);
    }
    else
    {
        return (false);
    }
}

bool StringC::IsSpecialChar(const char charValue)
{
    switch (charValue)
    {
        case '(':
        case ')':
        case '[':
        case ']':
        case '{':
        case '}':
        {
            return (true);
            break;
        }
        default:
        {
            return (false);
            break;
        }
    }
}


