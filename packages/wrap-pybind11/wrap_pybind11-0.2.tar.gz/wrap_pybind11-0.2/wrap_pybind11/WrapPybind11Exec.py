##
# File: WrapPybind11Exec.py
# Date: 2-Jan-2017
#
##
#
try:
    from WrapPybind11 import WrapPybind11
except:
    from wrap_pybind11.WrapPybind11 import WrapPybind11

import argparse

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
logger = logging.getLogger()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--module_name", dest="moduleName", default=None, help="Module name")
    parser.add_argument("--header_paths", dest="headerPathList", default=None, help="Header paths (comma separated list)")
    parser.add_argument("--config_path", dest="configFilePath", default=None, help="Configuration file path")
    parser.add_argument("--output_path", dest="outputPath", default=".", help="Output path for wrapped code")
    parser.add_argument("--export_json", dest="exportJson", default=False, action="store_true", help="Output path for wrapped code")

    args = parser.parse_args()
    #
    if args.headerPathList is None:
        hL = []
    else:
        hL = str(args.headerPathList).split(',')
    #
    mw = WrapPybind11(moduleName=args.moduleName, headerPathList=hL, configFilePath=args.configFilePath, outputPath=args.outputPath, exportJson=args.exportJson)
    mw.run()
    #


if __name__ == '__main__':
    main()
