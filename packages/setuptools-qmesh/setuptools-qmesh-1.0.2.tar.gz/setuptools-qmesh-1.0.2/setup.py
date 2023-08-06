#!/usr/bin/env python
#
#    Copyright (C) 2013 Alexandros Avdis and others.
#    See the AUTHORS.md file for a full list of copyright holders.
#
#    This file is part of setuptools-qmesh.
#
#    setuptools-qmesh is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    setuptools-qmesh is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with setuptools-qmesh.  If not, see <http://www.gnu.org/licenses/>.
'''Set-up script for installation and packaging of setuptools-qmesh.

This script facilitates installation and packaging of setuptools-qmesh, through standardised
procedures and utilities. This project need not be explicitly installed by a user:
setuptools-qmesh facilitates installation and packaging of other qmesh packages. In
particular, setuptools-qmesh introduces commands, setup-keywords and egg-info writers that
facilitate the correct operation, installation and packaging of other qmesh packages.
When ``pip`` is used, other qmesh packages will invoke installation of setuptools-qmesh.
In particular, a ``setuptools.setup`` call facilitates installation via ``pip``, or
``(sudo) python setup.py <command>``.
'''

def read(filename):
    '''Function reading file content.

    Function storing, and returning, file content as a string. Intended for reading the file
    containing the Version number and the read-me file during installation and packaging.

    Args:
        filename (str): Name of file to open and read contents.

    Returns:
        The file contents as a string (str).
    '''
    import os
    return open(os.path.join(os.path.dirname(__file__), filename)).read().strip()

def main():
    '''Function installing, packaging and testing the setuptools-qmesh package.

    This function makes a call to setuptools.setup, with appropriate arguments.
    '''
    import setuptools
    #Call setuptools setup() for installation, testing and packaging
    setuptools.setup(
        name='setuptools-qmesh',
        version=read('VERSION'),
        description="setuptools plugin for qmesh installation, packaging and testing",
        long_description=read('README.md'),
        author="The QMesh Development Team.",
        author_email="develop@qmesh.org",
        url="https://www.qmesh.org",
        download_url='https://bitbucket.org/qmesh-developers/setuptools-qmesh/commits/tag/v'+\
                     read('VERSION'),
        packages=setuptools.find_packages(),
        entry_points={
            "distutils.commands":[
                "install_non_pip = setuptools_qmesh.command.install_non_pip:InstallNonPip",
                "check_qgis      = setuptools_qmesh.command.check_qgis:CheckQgis",
                "check_gmsh      = setuptools_qmesh.command.check_gmsh:CheckGmsh"],
            "distutils.setup_keywords": [
                "check_non_pip        = setuptools_qmesh.dist:assert_non_pip",
                "install_pyrdm        = setuptools.dist:assert_bool",
                "pyrdm_path           = setuptools_qmesh.dist:assert_path",
                "qgis_path            = setuptools_qmesh.dist:assert_path",
                "gmsh_bin_path        = setuptools_qmesh.dist:assert_path",
                "include_git_sha_key  = setuptools.dist:assert_bool",
                "include_full_license = setuptools.dist:assert_bool",
                "include_author_ids   = setuptools.dist:assert_bool"],
            "egg_info.writers": [
                "QGIS_PATH     = setuptools_qmesh.command.egg_info:write_qgis_path",
                "GMSH_BIN_PATH = setuptools_qmesh.command.egg_info:write_gmsh_bin_path",
                "GIT_SHA_KEY   = setuptools_qmesh.command.egg_info:write_git_sha_key",
                "LICENSE       = setuptools_qmesh.command.egg_info:write_full_license",
                "AUTHORS.md    = setuptools_qmesh.command.egg_info:write_author_ids"],
            },
        license='GPLv3',
        install_requires=['GitPython'],
        package_data={'':['../VERSION', '../AUTHORS.md', '../GIT_SHA_KEY',
                          '../LICENSE', '../README.md']},
        test_suite="tests",
        keywords=['GIS', 'mesh generation', 'setuptools'],
        tests_require=['pylint', 'pyenchant',
                       'sphinxcontrib-bibtex', 'sphinxcontrib-napoleon'],
        extras_require=dict(build_doc=['sphinxcontrib-bibtex', 'sphinxcontrib-napoleon'])
        )

if __name__ == '__main__':
    main()
