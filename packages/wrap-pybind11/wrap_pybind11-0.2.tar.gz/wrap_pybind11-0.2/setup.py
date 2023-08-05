# File: setup.py
# Date: 2-Jan-2018 jdw.
#
# Package installation for module wrap_pybind11
#
import os
import re
import sys
import platform
import subprocess

from setuptools import setup, Extension, find_packages

from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion


class CMakeExtension(Extension):

    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):

    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        env['RUN_FROM_DISUTILS'] = "yes"
        #
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        #
        if False:
            print("------------------------------")
            print("Extension source path ", ext.sourcedir)
            print("CMAKE_ARGS ", cmake_args)
            print("self.build_temp ", self.build_temp)
            print("extdir", extdir)
            print("ext.name", ext.name)
            print("sys.executable", sys.executable)
            print("CXXFLAGS ", env['CXXFLAGS'])

        #
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)


packages = []
thisPackage = 'wrap_pybind11'
requires = ['CppHeaderParser', 'pybind11']


with open('wrap_pybind11/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


setup(
    name=thisPackage,
    version=version,
    description='Create Python wrapper for C++  header files using PyBind11.',
    long_description="See:  README.md",
    author='John Westbrook',
    author_email='john.westbrook@rcsb.org',
    url='http://www.rcsb.org',
    #
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ),
    entry_points={
        'console_scripts': [
            'wrap_pybind11_cli=wrap_pybind11.WrapPybind11Exec:main',
        ]
    },
    #
    install_requires=['CppHeaderParser', 'pybind11'],
    packages=find_packages(exclude=['tests.*', 'modules.*']),
    package_data={
        # If any package contains *.md or *.rst files, include them:
        '': ['*.md', '*.rst'],
    },
    #
    test_suite="wrap_pybind11.tests",
    tests_require=['tox'],
    #
    # Not configured ...
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    # Added for
    command_options={
        'build_sphinx': {
            'project': ('setup.py', thisPackage),
            'version': ('setup.py', version),
            'release': ('setup.py', version)
        }
    },
    ext_modules=[CMakeExtension('wrap_pybind11.wrap_pybind11')],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)
