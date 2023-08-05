//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$

#include <string>
#include <vector>

#include "Exceptions.h"
#include "StringB.h"


using std::string;
using std::vector;



const string StringB::UnknownValue("?");
const string StringB::InapplicableValue(".");

// Return by value
//

std::string StringB::methodCombine1(const string& categoryName,  const string& attribName)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "StringB::MakeCifItem");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name","StringB::MakeCifItem");
    }

    std::string cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
    return cifItem;
}

std::string StringB::methodCombine1(const string& categoryName,  const string& attribName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "StringB::MakeCifItem");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name","StringB::MakeCifItem");
    }

    std::string cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
    return cifItem;
}


// Update argument passed as reference with result -
void StringB::methodCombine2(string& cifItem, const string& categoryName,  const string& attribName)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "StringB::MakeCifItem");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name",  "StringB::MakeCifItem");
    }

    cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
}

void StringB::methodCombine2(string& cifItem, const string& categoryName,  const string& attribName, const std::string &PREFIX_CHAR, const std::string &JOIN_CHAR)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "StringB::MakeCifItem");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name",  "StringB::MakeCifItem");
    }

    cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
}


void StringB::methodCombine3(std::vector<std::string>& cifItems, const std::string& categoryName, const std::vector<std::string>& attribsNames)
{
    cifItems.assign(attribsNames.size(), string());

    for (unsigned int attribI = 0; attribI < attribsNames.size(); ++attribI)
    {
        methodCombine2(cifItems[attribI], categoryName, attribsNames[attribI]);
    }
}


const std::vector<std::string>& StringB::methodSetAndReturn4(const std::string& categoryName, const std::vector<std::string>& attribsNames)
{
    myStringVec.clear();
    myStringVec.assign(attribsNames.size(), string());

    for (unsigned int attribI = 0; attribI < attribsNames.size(); ++attribI)
    {
        methodCombine2(myStringVec[attribI], categoryName, attribsNames[attribI]);
    }
    return myStringVec;
}



bool StringB::IsEmptyValue(const string& value)
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

bool StringB::IsSpecialChar(const char charValue)
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


