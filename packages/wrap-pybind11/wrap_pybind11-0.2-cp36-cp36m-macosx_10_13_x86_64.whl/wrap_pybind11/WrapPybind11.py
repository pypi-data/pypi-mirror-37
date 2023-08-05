##
# File:    WrapPybind11.py
# Author:  J. Westbrook
# Date:    29-Dec-2017
# Version: 0.001
#
# Updates:
#   31-Dec-2017 jdw reproduce workbench examples, produced compiled library passing
#                   all unit tests.
#   4-Jan-2018  jdw rename and adapt as a separate package --
#   7-Jan-2018  jdw multiple extensions to support complexity of the cifparse library -
#  14-Oct-2018  jdw add support for a single header specific namespace
##
"""
Make python wrapper for C++  header files using PyBind11.

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"
__version__ = "V0.01"

import os
import datetime
import collections
import CppHeaderParser

import configparser

import logging
logger = logging.getLogger(__name__)


def serializer_helper(obj):
    data = {'__class__': obj.__class__.__name__,
            '__module__': obj.__module__
            }
    data.update(obj.__dict__)
    #    return data  # data is dict object in this case
    return ''


class WrapConfig:

    def __init__(self, configPath, sectionName='DEFAULT'):
        self.__cD = {}
        self.__cD = self.__rdConfigFile(configPath, sectionName)

    def __getConfig(self, configPath, sectionName):
        self.__cD = self.__rdConfigFile(configPath, sectionName)

    def getTypeExcludes(self):
        exL = []
        if 'exclude_types' in self.__cD:
            exL = str(self.__cD['exclude_types']).split(',')
        #
        return exL

    def getMethodExcludes(self):
        exL = []
        mL = []
        try:
            if 'exclude_methods' in self.__cD:
                exL = str(self.__cD['exclude_methods']).split(',')
            #
            mL = [tuple(cm.split('::')) for cm in exL]
        except Exception as e:
            logger.exception("Failing with exception %s" % str(e))
        #
        return mL

    def getClassExcludes(self):
        exL = []
        if 'exclude_classes' in self.__cD:
            exL = str(self.__cD['exclude_classes']).split(',')
        #
        return exL

    def getHeaderPaths(self):
        hL = []
        if 'header_paths' in self.__cD:
            hL = str(self.__cD['header_paths']).split(',')
        #
        return hL

    def getHeadeNamespaceD(self):
        hL = []
        if 'header_paths' in self.__cD:
            hL = str(self.__cD['header_paths']).split(',')
        nL = []
        if 'header_namespaces' in self.__cD:
            nL = str(self.__cD['header_namespaces']).split(',')
        #
        nsD = {}
        if len(nL) == len(hL):
            for ii, h in enumerate(hL):
                nsD[h] = nL[ii]

        return nsD

    def getQualifiedTypes(self):
        qL = []
        if 'qualified_types' in self.__cD:
            qL = str(self.__cD['qualified_types']).split(',')
        #
        tupL = [tuple(q.split('|')) for q in qL]

        return tupL

    def __rdConfigFile(self, configPath, sectionName):
        try:
            config = configparser.ConfigParser()
            config.sections()
            config.read(configPath)
            #
            if sectionName in config:
                logger.info("Configuration options %s" % ([k for k in config[sectionName]]))
                return config[sectionName]
            else:
                return {}
        except Exception as e:
            logger.error("Failed processing configuration file %s section %s " % (configPath, sectionName))
        return {}


class WrapPybind11:

    def __init__(self, moduleName, headerPathList=None, configFilePath=None, outputPath=None, exportJson=False):
        self.__moduleName = moduleName
        self.__headerPathList = headerPathList
        self.__outputPath = outputPath if outputPath is not None else '.'
        self.__exportJson = exportJson
        self.__classExcludeList = []
        self.__typeExcludeList = []
        self.__methodExcludeList = []
        self.__qualifiedTypeList = []
        self.__headerNamespaceD = {}
        if configFilePath is not None and os.access(configFilePath, os.R_OK):
            self.__cfObj = WrapConfig(configPath=configFilePath, sectionName=self.__moduleName)
            self.__classExcludeList = self.__cfObj.getClassExcludes()
            self.__methodExcludeList = self.__cfObj.getMethodExcludes()
            self.__typeExcludeList = self.__cfObj.getTypeExcludes()
            self.__qualifiedTypeList = self.__cfObj.getQualifiedTypes()
            if self.__headerPathList is None or len(self.__headerPathList) == 0:
                self.__headerPathList = self.__cfObj.getHeaderPaths()
            self.__headerNamespaceD = self.__cfObj.getHeadeNamespaceD()
        #

    def __wrModuleWrapper(self, moduleName, headerPathList):
        """
        """
        #
        hL = []
        for hp in headerPathList:
            dn, fn = os.path.split(hp)
            h, ext = os.path.splitext(fn)
            hL.append(h)
        logger.debug("Module wrapper header list: {}".format(hL))
        # Module file
        dts = datetime.datetime.today().strftime('%Y-%m-%d')
        mfn = os.path.join(self.__outputPath, 'wrap' + self.__moduleName + '.cpp')
        with open(mfn, 'w') as mfh:
            mfh.write("// File: %s\n" % mfn)
            mfh.write("// Date: %s\n" % dts)
            mfh.write("//\n")
            mfh.write("#include <pybind11/pybind11.h>\n")
            mfh.write("#include <pybind11/stl.h>\n")
            mfh.write("namespace py = pybind11;\n")
            mfh.write("using namespace pybind11::literals;\n")
            mfh.write("\n")
            #
            for h in hL:
                mfh.write("void wrap%s(py::module &);\n" % h)
            #
            mfh.write("\n")

            mfh.write("PYBIND11_MODULE(%s, m) {\n" % moduleName)
            for h in hL:
                mfh.write("wrap%s(m);\n" % h)
            mfh.write("}\n")

    def __wrapEnum(self, enum, className=None, varName=None):

        name = enum['name']
        typename = name
        parent = 'm'

        if className:
            typename = '%s::%s' % (className, typename)
            parent = varName if varName is not None else className.lower()

        #
        ret = ['py::enum_<%s>(%s, "%s")' % (typename, parent, name)]

        for v in enum['values']:
            k = v['name']
            ret.append('  .value("%s", %s::%s)' % (k, typename, k))

        ret[-1] = ret[-1] + ';'
        return ret

    def __hasExcludedType(self, pTypes):
        for typ in self.__typeExcludeList:
            for pT in pTypes:
                if typ in pT:
                    return True
        return False

    def __isExcludedMethod(self, className, methodName):
        for mTup in self.__methodExcludeList:
            if mTup[0] == className and mTup[1] == methodName:
                return True
        return False

    def __subsMethodName(self, methName):
        ret = methName
        if methName == 'operator=':
            ret = 'assign'
        elif methName == 'operator==':
            ret = '__eq__'
        elif methName == 'operator()':
            ret = '__call__'
        #  More could be included
        return ret

    def __updateTypes(self, className, methObj):
        methName = methObj['name']
        # Reset types for enums
        for p in methObj['parameters']:
            if p.get('enum'):
                p['raw_type'] = p['enum']
                if p['constant']:
                    p['type'] = 'const ' + p['enum']
                else:
                    p['type'] = p['enum']
                logger.info("ENUM enum %s raw_type %s type %s" % (p['enum'], p['raw_type'], p['type']))
            logger.info("UPDATETYPES INIT className %s methName %s raw_type %s type %s" % (className, methName, p['raw_type'], p['type']))
            for qT in self.__qualifiedTypeList:
                if qT[0] == className and qT[1] == methName and p['type'] == qT[2]:
                    p['type'] = qT[3]
                    logger.info("UPDATETYPES FINAL raw_type %s type %s" % (p['raw_type'], p['type']))
        #
        #  Use new configuration ---
        #logger.debug("Qualified types %r" % self.__qualifiedTypeList)
        if (False):
            for qT in self.__qualifiedTypeList:
                for p in methObj['parameters']:
                    logger.info("UPDATETYPES raw_type %s type %s" % (p['raw_type'], p['type']))
                    tL = p['type'].split()
                    for i in range(len(tL)):
                        if tL[i] in qT:
                            tL[i] = qT
                    p['type'] = ' '.join(tL)
        #

    def __wrapMethod(self, className, varName, methObj, overloaded=False):

        # no wrappers for destructors
        if methObj.get('destructor', False):
            return []

        ret = []
        methName = methObj['name']
        methNamePy = self.__subsMethodName(methName)
        if self.__isExcludedMethod(className, methName):
            return []
        isOperator = methObj['operator']
        parameters = methObj['parameters']
        returnType = methObj['rtnType'].replace('inline ', '').replace('static ', '')
        if (False):
            if returnType.startswith('inline'):
                returnType.replace('inline', '')
            if returnType.startswith('static '):
                returnType.replace('static', '')
        #
        if methObj.get('returns_enum') and '::' not in returnType:
            # test for a qualified enum -
            returnType = className + '::' + returnType
        #
        mStatic = ''
        if methObj['static']:
            mStatic = '_static'
        mutableParam = False
        refs = [p for p in parameters if p['reference'] and not p['constant']]
        if refs:
            mutableParam = True

        logger.debug("method name {} parameters {}".format(methName, [(p['name'], p['raw_type']) for p in parameters]))

        # Reset types for enums
        if False:
            for p in parameters:
                if p.get('enum'):
                    p['raw_type'] = p['enum']
                    if p['constant']:
                        p['type'] = 'const ' + p['enum']
                    else:
                        p['type'] = p['enum']

        else:
            self.__updateTypes(className, methObj)

        #
        pTypes = []
        for p in parameters:
            if p['raw_type'] == "::" + className:
                pT = className + " const &"
                pTypes.append(pT)
            else:
                pTypes.append(p['type'])

        ##
        logger.debug("EXCLUDED types %r" % self.__typeExcludeList)
        ##
        for pType in pTypes:
            logger.info("className %s methodName %s pType %s" % (className, methName, pType))
        ##
        if self.__hasExcludedType(pTypes):
            logger.info("Skipping method %s.%s with excluded type." % (className, methName))
            return []

        #  Special handling of constructors
        #  cl.def(pybind11::init([](){ return new TableFile(); }), "doc");
        #  #
        if methName == className:
            params = ','.join(pTypes)
            pNames = ','.join('py::arg("' + p['name'] + '")' for p in parameters)
            if len(params) > 0:
                logger.info("INIT params %r" % params)
                ret.append('  %s.def(py::init<%s>(),%s);' % (varName, params, pNames))
            else:
                ret.append('  %s.def(py::init<>());' % varName)
            #
        else:

            methReturnValues = []
            methReturnString = ''
            if methObj['returns'] != 'void':
                methReturnValues.append('_retVal')
                methReturnString = returnType + ' _retVal = '

            if mutableParam and not isOperator:
                methParams = ''
                pList = []
                nList = []
                for p in parameters:
                    if p['type'] == 'void':
                        continue
                    # JDW filter types and nanes consistently
                    if False:
                        qualifier = ' '
                        if p['reference']:
                            qualifier = ' &'
                        elif p['pointer']:
                            qualifier = ' *'
                        if p['constant']:
                            pList.append('const ' + p['raw_type'] + qualifier + p['name'])
                        else:
                            pList.append(p['raw_type'] + qualifier + p['name'])
                    else:
                        pList.append(p['type'] + ' ' + p['name'])
                        nList.append(p['name'])
                        if ((p['reference'] or p['pointer']) and not p['constant']):
                            methReturnValues.append(p['name'])

                if len(pList) > 0:
                    methParams = ', ' + ', '.join(pList)
                #
                ret.append('  %s.def%s("%s", [](%s &o %s) {' % (varName, mStatic, methName, className, methParams))

                methParamNames = ', '.join(nList)

                ret.append('    %s o.%s(%s);' % (methReturnString, methName, methParamNames))

                #methReturnValues.extend(p['name'] for p in methObj['parameters'] if (p['reference'] or p['pointer']) and not p['constant'])

                if len(methReturnValues) == 0:
                    pass
                elif len(methReturnValues) == 1:
                    ret.append('    return %s;' % methReturnValues[0])
                else:
                    ret.append('    return std::make_tuple(%s);' % ', '.join(methReturnValues))

                mdoc = '%s with arguments %s' % (methName, methParamNames)
                if nList:
                    pNames = ', ' + ', '.join('py::arg("' + name + '")' for name in nList)
                else:
                    pNames = ''
                ret.append('  },"%s" %s);' % (mdoc, pNames))

            else:

                overload = ''
                mdoc = ''
                pList = []
                nList = []
                for p in parameters:
                    if p['type'] == 'void':
                        continue
                    #
                    if False:
                        qualifier = ' '
                        if p['reference']:
                            qualifier = ' &'
                        elif p['pointer']:
                            qualifier = ' *'
                        if p['raw_type'] == "::" + className:
                            pT = 'class ' + className
                        else:
                            pT = p['raw_type']
                        if p['constant']:
                            pList.append('const ' + pT + qualifier)
                        else:
                            pList.append(pT + qualifier)
                    else:
                        pList.append(p['type'])
                        nList.append(p['name'])

                pNames = ', '.join('py::arg("' + name + '")' for name in nList)

                if overloaded or ('bool' in returnType):
                    # overloaded method
                    params = ', '.join(pList)
                    #
                    cQual = ''
                    if methObj['const']:
                        cQual = ' const '

                    if methObj['static']:
                        overload = '(%s (*)(%s)%s) ' % (returnType, params, cQual)
                    else:
                        overload = '(%s (%s::*)(%s)%s) ' % (returnType, className, params, cQual)
                    mdoc = '%s with arguments %s' % (methName, params)
                if len(pNames) > 0:
                    ret.append('  %s.def%s("%s", %s&%s::%s,"%s",%s);' % (varName, mStatic, methNamePy, overload, className, methName, mdoc, pNames))
                else:
                    ret.append('  %s.def%s("%s", %s&%s::%s,"%s");' % (varName, mStatic, methNamePy, overload, className, methName, mdoc))

        return ret

    def __wrapClass(self, classObj):

        className = classObj['name']
        varName = 'cls'
        #
        inheritList = classObj.get('inherits')
        cL = []
        for inhD in inheritList:
            cL.append(inhD['class'])
        #
        # std::shared_ptr<className>
        #
        ret = ['{']
        # ret.append(' py::class_<%s> %s(m, "%s", "Wrapper for class %s");' % (className, varName, className, className))
        if cL:
            ret.append(' py::class_<%s, std::shared_ptr<%s>, %s> %s(m, "%s", "Wrapper for class %s");' % (className, className, ','.join(cL), varName, className, className))
        else:
            ret.append(' py::class_<%s, std::shared_ptr<%s>> %s(m, "%s", "Wrapper for class %s");' % (className, className, varName, className, className))
        #

        for e in classObj['enums']['public']:
            ret.append('')
            ret += self.__indentList(self.__wrapEnum(e, className=className, varName=varName))
        ret.append('')
        #
        pmD = {}
        privateMethods = classObj['methods']['private']
        for meth in privateMethods:
            pmD[meth['name']] = True
        #
        methods = classObj['methods']['public']
        if methods:

            # overloaded methods -
            meths = collections.OrderedDict()
            for meth in methods:
                meths.setdefault(meth['name'], []).append(meth)

            for ml in meths.values():
                if len(ml) == 1:
                    if ml[0]['name'] in pmD or ml[0]['operator']:
                        ret += self.__wrapMethod(className, varName, ml[0], True)
                    else:
                        ret += self.__wrapMethod(className, varName, ml[0])
                else:
                    for mh in ml:
                        ret += self.__wrapMethod(className, varName, mh, True)
        ret.append('}')
        #
        return ret

    def __wrapFunctions(self, functions):
        #
        varName = 'm'
        ret = []
        if functions:
            # overloaded functions -
            funcs = collections.OrderedDict()
            for f in functions:
                funcs.setdefault(f['name'], []).append(f)

            for fl in funcs.values():
                if len(fl) == 1:
                    ret += self.__wrapFunction(varName, fl[0])
                else:
                    for fh in fl:
                        ret += self.__wrapFunction(varName, fh, True)
        return ret

    def __wrapFunction(self, varName, funcObj, overloaded=False):

        ret = []
        funcName = funcObj['name']
        parameters = funcObj['parameters']
        mStatic = ''
        if funcObj['static']:
            mStatic = '_static'
        mutableParam = False
        refs = [p for p in parameters if p['reference'] and not p['constant']]
        if refs:
            mutableParam = True

        logger.debug("function name {} parameters {}".format(funcName, [(p['name'], p['raw_type']) for p in parameters]))

        # Reset types for enums
        for p in parameters:
            if p.get('enum'):
                p['raw_type'] = p['enum']
                p['type'] = p['enum']

        #
        pTypes = [p['raw_type'] for p in parameters]
        if self.__hasExcludedType(pTypes):
            logger.debug("Skipping function %s with excluded type." % (funcName))
            return []

        funcReturnValues = []
        if funcObj['returns'] != 'void':
            funcReturnValues.append('_retVal')

        if mutableParam:
            funcParams = ''
            pS = []
            for p in parameters:
                qualifier = ' '
                if p['reference']:
                    qualifier = ' &'
                elif p['pointer']:
                    qualifier = ' *'
                #
                if p['constant']:
                    pS.append('const ' + p['raw_type'] + qualifier + p['name'])
                else:
                    pS.append(p['raw_type'] + qualifier + p['name'])
            if len(pS) > 0:
                funcParams = ', '.join(pS)
            #
            ret.append('  %s.def%s("%s", [](%s) {' % (varName, mStatic, funcName, funcParams))

            funcParamNames = ', '.join(p['name'] for p in funcObj['parameters'])

            funcReturnString = 'auto _retVal = '
            if '_retVal' not in funcReturnValues:
                funcReturnString = ''

            ret.append('    %s %s(%s);' % (funcReturnString, funcName, funcParamNames))

            funcReturnValues.extend(p['name'] for p in funcObj['parameters'] if (p['reference'] or p['pointer']) and not p['constant'])

            if len(funcReturnValues) == 0:
                pass
            elif len(funcReturnValues) == 1:
                ret.append('    return %s;' % funcReturnValues[0])
            else:
                ret.append('    return std::make_tuple(%s);' % ', '.join(funcReturnValues))

            mdoc = '%s with arguments %s' % (funcName, funcParamNames)
            pNames = ', '.join('py::arg("' + p['name'] + '")' for p in parameters)
            ret.append('  },"%s", %s);' % (mdoc, pNames))

        else:

            overload = ''
            mdoc = ''
            pNames = ', '.join('py::arg("' + p['name'] + '")' for p in parameters)
            if overloaded or ('bool' in funcObj['returns']):
                # overloaded funcod
                # params = ','.join(p['raw_type'] for p in parameters)
                pS = []
                for p in parameters:
                    qualifier = ' '
                    if p['reference']:
                        qualifier = ' &'
                    elif p['pointer']:
                        qualifier = ' *'
                    if p['constant']:
                        pS.append('const ' + p['raw_type'] + qualifier)
                    else:
                        pS.append(p['raw_type'] + qualifier)
                params = ', '.join(pS)
                #
                if funcObj['static']:
                    overload = '(%s (*)(%s))' % (funcObj['returns'], params)
                else:
                    overload = '(%s (*)(%s))' % (funcObj['returns'], params)
                mdoc = '%s with arguments %s' % (funcName, params)
            if len(parameters) > 0:
                ret.append('  %s.def%s("%s", %s &%s, "%s", %s);' % (varName, mStatic, funcName, overload, funcName, mdoc, pNames))
            else:
                ret.append('  %s.def%s("%s", %s &%s, "%s");' % (varName, mStatic, funcName, overload, funcName, mdoc))

        return ret

    def __export_header(self, headerPath, hObj):
        # serializer_helper
        dn, fn = os.path.split(headerPath)
        #
        fn = os.path.join(self.__outputPath, fn + '.json')
        with open(fn, 'w') as ofh:
            ofh.write(self.__toJSON(hObj))

    def __toJSON(self, obj, indent=2):
        """Converts a parsed structure to JSON"""
        obj.strip_parent_keys()
        try:
            del obj.__dict__["classes_order"]
        except Exception:
            pass
        # return json.dumps(obj.__dict__, indent=indent, check_circular=True, default=serializer_helper)
        return self.__dumps(obj.__dict__, indent=indent)

    def __dumps(self, value, indent=4):
        import re
        kwargs = dict(indent=indent, sort_keys=True)
        try:
            import json
            info = json.dumps(value, **kwargs)
        except Exception:
            # JSON doesn't like circular references :/
            try:
                string_repr = repr(value)
                # Replace python primitives, single-quotes, unicode, etc
                string_repr = string_repr\
                    .replace('None', 'null')\
                    .replace('True', 'true')\
                    .replace('False', 'false')\
                    .replace("u'", "'")\
                    .replace("'", '"')

                # Replace object and function repr's like <MyObject ...>
                string_repr = re.sub(r':(\s+)(<[^>]+>)', r':\1"\2"', string_repr)

                # Replace tuples with lists, very naively
                string_repr = string_repr.replace('(', '[').replace(')', ']')

                info = json.dumps(json.loads(string_repr), **kwargs)
            except Exception:
                from pprint import pformat
                info = pformat(value, indent=indent)

        return info

    def __indentList(self, vL, indent='   '):
        return [indent + v for v in vL]

    def __wrap_header(self, headerPath, classExcludeList):

        dn, fn = os.path.split(headerPath)
        h, ext = os.path.splitext(fn)
        #
        hObj = CppHeaderParser.CppHeader(headerPath)
        if self.__exportJson:
            self.__export_header(headerPath, hObj)
        #
        oL = []
        oL.append("#include <pybind11/pybind11.h>")
        oL.append("#include <pybind11/stl.h>")
        for inc in hObj.includes:
            oL.append("#include {}".format(inc))
        #
        oL.append('#include "{}.h"'.format(h))

        #
        oL.append("namespace py = pybind11;")
        oL.append("using namespace pybind11::literals;")
        oL.append("")
        if headerPath in self.__headerNamespaceD:
            oL.append("using namespace %s;" % self.__headerNamespaceD[headerPath])
        #
        oL.append("")
        oL.append("void wrap%s(py::module &m) {" % h)
        oL.append('   m.doc() = "Wrapper for header file %s";' % fn)
        oL.append("")

        #
        # wrap out of class enums -
        for e in hObj.enums:
            oL += self.__indentList(self.__wrapEnum(e))
            oL.append('')

        #
        oL += self.__indentList(self.__wrapFunctions(hObj.functions))

        for classObj in sorted(hObj.classes.values(), key=lambda c: c['line_number']):
            if classObj['name'] in classExcludeList:
                continue
            oL += self.__indentList(self.__wrapClass(classObj))

            oL.append('')
        #
        oL.append("}")

        return oL

    def __wrHeaderWrapper(self, headerPath, cL):
        dn, fn = os.path.split(headerPath)
        h, ext = os.path.splitext(fn)
        # Header wrapper file
        dts = datetime.datetime.today().strftime('%Y-%m-%d')
        cfn = os.path.join(self.__outputPath, 'wrap' + h + '.cpp')
        with open(cfn, 'w') as cfh:
            cfh.write("// File: %s\n" % cfn)
            cfh.write("// Date: %s\n" % dts)
            cfh.write("//\n")
            cfh.write("\n")
            cfh.write('\n'.join(cL))

    def run(self):
        return self.__run(self.__moduleName, self.__headerPathList, self.__classExcludeList)

    def __run(self, moduleName, headerPathList, classExcludeList):
        oL = []
        excL = classExcludeList if classExcludeList is not None else []
        #
        self.__wrModuleWrapper(moduleName, headerPathList)
        #
        for headerPath in headerPathList:
            oL = self.__wrap_header(headerPath, excL)
            self.__wrHeaderWrapper(headerPath, oL)

        #
        return True
