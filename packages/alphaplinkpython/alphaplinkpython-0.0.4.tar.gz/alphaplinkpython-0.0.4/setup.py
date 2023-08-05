# Cython compile instructions

from setuptools import setup
from Cython.Build import cythonize

from setuptools import Extension, find_packages
import numpy
import glob
import shutil
import os
from sys import platform
import sys
import sysconfig
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), './alphaplinkpython/alphaplink/cpp_src')))

# move pxd files to correct folder


libLocation = "alphaplinkpython."


# Use python setup.py build_ext --inplace
# to compile
cpp_src_dir = "alphaplinkpython/alphaplink/"
cython_src_dir = "alphaplinkpython/cpp_src/"
compile_args = ["-std=c++11", "-g"]
link_args = ["-std=c++11", "-g"]

# for file in glob.glob(cpp_src_dir+'*.pxd'):
#     print(file)
#     shutil.copy(file, 'alphahousepython')

# 'magic' to make it play nice with OS X compilers
if sys.platform == "darwin":
    try:
        cc = sysconfig.get_config_var('CC')
        # might still be clang
        if (cc == 'gcc'):
            newCC = os.environ["CC"]
            if (newCC == 'gcc' or newCC == 'g++' or 'clang' in newCC or newCC == ''):
                os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
                compile_args.append("-stdlib=libc++")
                compile_args.append("-Xpreprocessor")
                compile_args.append("-fopenmp")
                compile_args.append("-lomp")
                link_args.append("-stdlib=libc++")
                link_args.append("-Xpreprocessor")
                link_args.append("-fopenmp")
                link_args.append("-lomp")
                link_args.append("/usr/local/opt/libomp/lib/libgomp.a")
            elif (newCC == 'icpc' or newCC == 'icc'):
                compile_args.append("-qopenmp")
                link_args.append("-qopenmp")
            else:  # This is probably a custom GCC version
                link_args.append("-fopenmp")
                # link_args.append("-lomp")
                # compile_args.append("-lomp")
                compile_args.append("-fopenmp")
    except KeyError:
        # default is likely
        os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
        compile_args.append("-stdlib=libc++")
        link_args.append("-stdlib=libc++")


plinkWriter = Extension(
    libLocation+"PlinkWriter",
    language="c++",
    include_dirs=[cpp_src_dir, cython_src_dir],
    extra_compile_args=compile_args,
    extra_link_args=link_args,
    sources=[cython_src_dir+"PlinkWriter.pyx", cpp_src_dir+'PlinkWriter.cpp', cpp_src_dir+'BitHolder.cpp',
             cpp_src_dir+'PlinkType.cpp']
)
plinkType = Extension(
    libLocation+"PlinkType",
    language="c++",
    include_dirs=[cpp_src_dir, cython_src_dir],
    extra_compile_args=compile_args,
    extra_link_args=link_args,
    sources=[cython_src_dir+"PlinkType.pyx",
             cpp_src_dir+'PlinkType.cpp']
)


ext_modules = [plinkWriter, plinkType]

setup(
    name="alphaplinkpython",
    license='GPL',
    author='david',
    author_email='david.wilson@roslin.ed.ac.uk',
    version='0.0.4',
    description='AlphaGenes library for dealitng with plink',
    ext_modules=cythonize(ext_modules, gdb_debug=True),
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    package_data={'alphaplinkpython': [cpp_src_dir+'*.pxd']},
    include_package_data=False,
    include_dirs=[numpy.get_include()],
    setup_requires=[
        # Note bug noted here: https://github.com/cython/cython/issues/1953 might require cython < 0.26
        "cython >= 0.26",
        "numpy",
    ],
    install_requires=[
        'numpy',
        'cython >= 0.26',
    ]
)
