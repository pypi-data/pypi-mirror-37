//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$

#include <string>
#include <vector>

#include "Exceptions.h"
#include "StringA.h"


using std::string;
using std::vector;



const string StringA::UnknownValue("?");
const string StringA::InapplicableValue(".");

// Return by value
//

std::string StringA::methodCombine1(const string& categoryName,  const string& attribName)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "StringA::MakeCifItem");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name","StringA::MakeCifItem");
    }

    std::string cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
    return cifItem;
}

// Update argument passed as reference with result -
void StringA::methodCombine2(string& cifItem, const string& categoryName,  const string& attribName)
{
    if (categoryName.empty())
    {
        throw EmptyValueException("Empty category name", "StringA::MakeCifItem");
    }

    if (attribName.empty())
    {
        throw EmptyValueException("Empty attribute name",  "StringA::MakeCifItem");
    }

    cifItem = PREFIX_CHAR + categoryName + JOIN_CHAR + attribName;
}


void StringA::methodCombine3(std::vector<std::string>& cifItems, const std::string& categoryName, const std::vector<std::string>& attribsNames)
{
    cifItems.assign(attribsNames.size(), string());

    for (unsigned int attribI = 0; attribI < attribsNames.size(); ++attribI)
    {
        methodCombine2(cifItems[attribI], categoryName, attribsNames[attribI]);
    }
}


const std::vector<std::string>& StringA::methodSetAndReturn4(const std::string& categoryName, const std::vector<std::string>& attribsNames)
{
    myStringVec.clear();
    myStringVec.assign(attribsNames.size(), string());

    for (unsigned int attribI = 0; attribI < attribsNames.size(); ++attribI)
    {
        methodCombine2(myStringVec[attribI], categoryName, attribsNames[attribI]);
    }
    return myStringVec;
}



bool StringA::IsEmptyValue(const string& value)
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

bool StringA::IsSpecialChar(const char charValue)
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


