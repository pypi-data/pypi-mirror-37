# import os
# import re
# import sys
# import platform
# import subprocess
#
# from setuptools import setup, Extension
# from setuptools.command.build_ext import build_ext
# from distutils.version import LooseVersion
#
#
# class CMakeExtension(Extension):
#     def __init__(self, name, sourcedir=''):
#         Extension.__init__(self, name, sources=[])
#         self.sourcedir = os.path.abspath(sourcedir)
#
#
# class CMakeBuild(build_ext):
#     def run(self):
#         try:
#             out = subprocess.check_output(['cmake', '--version'])
#         except OSError:
#             raise RuntimeError("CMake must be installed to build the following extensions: " +
#                                ", ".join(e.name for e in self.extensions))
#
#         if platform.system() == "Windows":
#             cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
#             if cmake_version < '3.1.0':
#                 raise RuntimeError("CMake >= 3.1.0 is required on Windows")
#
#         for ext in self.extensions:
#             self.build_extension(ext)
#
#     def build_extension(self, ext):
#         extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
#         cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
#                       '-DPYTHON_EXECUTABLE=' + sys.executable]
#
#         cfg = 'Debug' if self.debug else 'Release'
#         build_args = ['--config', cfg]
#
#         if platform.system() == "Windows":
#             cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
#             if sys.maxsize > 2**32:
#                 cmake_args += ['-A', 'x64']
#             build_args += ['--', '/m']
#         else:
#             cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
#             build_args += ['--', '-j2']
#
#         env = os.environ.copy()
#         env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
#                                                               self.distribution.get_version())
#         if not os.path.exists(self.build_temp):
#             os.makedirs(self.build_temp)
#         subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
#         subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)
#
# setup(
#     name='vgram',
#     version='0.1.2',
#     author='Khvorov Aleksandr',
#     author_email='khvorov.aleksandr@gmail.com',
#     description='V-gram builder library',
#     long_description='Dictionary of v-gram construction',
#     url='https://github.com/akhvorov/vgram',
#     ext_modules=[CMakeExtension('vgram')],  # ext_modules=[CMakeExtension('vgram')],
#     cmdclass=dict(build_ext=CMakeBuild),
#     zip_safe=False,
# )

from setuptools import setup, Extension, Distribution
import setuptools.command.build_ext

import sys
import sysconfig
import os
import os.path
import distutils.sysconfig

import itertools
from glob import iglob


def _get_vgram_builder_libname():
    builder = setuptools.command.build_ext.build_ext(Distribution())
    full_name = builder.get_ext_filename('libvgram_builder')
    without_lib = full_name.split('lib', 1)[-1]
    without_so = without_lib.rsplit('.so', 1)[0]
    return without_so


def _get_distutils_build_directory():
    """
    Returns the directory distutils uses to build its files.
    We need this directory since we build extensions which have to link
    other ones.
    """
    pattern = "lib.{platform}-{major}.{minor}"
    return os.path.join('build', pattern.format(platform=sysconfig.get_platform(),
                                                major=sys.version_info[0],
                                                minor=sys.version_info[1]))


def _get_source_files(directory):
    path = os.path.join('src', directory)
    iterable_sources = (iglob(os.path.join(root,'*.cc')) for root, dirs, files in os.walk(path))
    source_files = itertools.chain.from_iterable(iterable_sources)
    return list(source_files)


def _remove_strict_prototype_option_from_distutils_config():
    strict_prototypes = '-Wstrict-prototypes'
    config = distutils.sysconfig.get_config_vars()
    for key, value in config.items():
        if strict_prototypes in str(value):
            config[key] = config[key].replace(strict_prototypes, '')


_remove_strict_prototype_option_from_distutils_config()


# class _deferred_pybind11_include(object):
#     def __str__(self):
#         import pybind11
#         return pybind11.get_include()


extra_compile_args = []
# hidden_visibility_args = []
# include_dirs = ['include/', _deferred_pybind11_include()]

library_dirs = [_get_distutils_build_directory()]
python_module_link_args = []
base_library_link_args = []

if sys.platform == 'darwin':
    extra_compile_args.append('--std=c++11')
    extra_compile_args.append('--stdlib=libc++')
    extra_compile_args.append('-mmacosx-version-min=10.9')
    # hidden_visibility_args.append('-fvisibility=hidden')
    # include_dirs.append(os.getenv('UNIXODBC_INCLUDE_DIR', '/usr/local/include/'))
    # library_dirs.append(os.getenv('UNIXODBC_LIBRARY_DIR', '/usr/local/lib/'))

    from distutils import sysconfig
    vars = sysconfig.get_config_vars()
    vars['LDSHARED'] = vars['LDSHARED'].replace('-bundle', '')
    python_module_link_args.append('-bundle')
    builder = setuptools.command.build_ext.build_ext(Distribution())
    full_name = builder.get_ext_filename('libvgram')
    base_library_link_args.append('-Wl,-dylib_install_name,@loader_path/{}'.format(full_name))
    base_library_link_args.append('-dynamiclib')
    # odbclib = 'odbc'
elif sys.platform == 'win32':
    extra_compile_args.append('-DNOMINMAX')
    # odbclib = 'odbc32'
else:
    extra_compile_args.append('--std=c++11')
    # hidden_visibility_args.append('-fvisibility=hidden')
    python_module_link_args.append("-Wl,-rpath,$ORIGIN")
    # if 'UNIXODBC_INCLUDE_DIR' in os.environ:
    #     include_dirs.append(os.getenv('UNIXODBC_INCLUDE_DIR'))
    # if 'UNIXODBC_LIBRARY_DIR' in os.environ:
    #     library_dirs.append(os.getenv('UNIXODBC_LIBRARY_DIR'))
    # odbclib = 'odbc'


def get_extension_modules():
    extension_modules = []

    """
    Extension module which is actually a plain C++ library without Python bindings
    """
    vgram_builder_sources = _get_source_files('core')
    vgram_builder_library = Extension('libvgram_builder',
                                 sources=vgram_builder_sources,
                                 #include_dirs=include_dirs,
                                 extra_compile_args=extra_compile_args,
                                 extra_link_args=base_library_link_args,
                                 libraries=[],
                                 library_dirs=library_dirs)
    if sys.platform == "win32":
        vgram_builder_libs = []
    else:
        vgram_builder_libs = [_get_vgram_builder_libname()]
        extension_modules.append(vgram_builder_library)

    """
    An extension module which contains the main Python bindings for vgram
    """
    vgram_python_sources = _get_source_files('binding')
    if sys.platform == "win32":
        vgram_python_sources = vgram_builder_sources + vgram_python_sources
    vgram_python = Extension('pyvgram',
                                sources=vgram_python_sources,
                                #include_dirs=include_dirs,
                                extra_compile_args=extra_compile_args, # + hidden_visibility_args,
                                libraries=vgram_builder_libs,
                                extra_link_args=python_module_link_args,
                                library_dirs=library_dirs)
    extension_modules.append(vgram_python)
    return extension_modules


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()


setup(
    name='vgram',
    version='0.1.2',
    author='Khvorov Aleksandr',
    author_email='khvorov.aleksandr@gmail.com',
    description='V-gram builder library',
    long_description=long_description,
    url='https://github.com/akhvorov/vgram',
    include_package_data=True,
    packages=['core'],  # binding
    ext_modules=get_extension_modules(),
    install_requires=['pybind11>=2.2.0']
)
