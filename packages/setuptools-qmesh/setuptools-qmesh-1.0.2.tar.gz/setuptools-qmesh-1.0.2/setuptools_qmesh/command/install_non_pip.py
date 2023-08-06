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
''' Module with setuptools.Command-derived class, checking and installing non-pip packages.
'''

from setuptools import Command


class InstallNonPip(Command):
    '''Check non-PyPI packages are installed on the host system, attempt to install if not.

    qmesh depends on several python packages that are not distributed via the Python Package Index
    (PyPI). The purpose of this class is to ensure such Python packages are installed. If a package
    is not installed on the host system, it is downloaded and installed. In case of problems, the
    installation is halted, and the user is informed. This class is derived from the ``setuptools``
    Command class, to implement the necessary functionality in a way consistent to the
    ``setuptools`` packaging and distribution design, and to make the necessary checks at
    particular stages during the installation of qmesh packages.
    '''
    description = \
      'Check non-PyPI packages are installed on the host system, and attempt to install if not.'
    user_options = [('install-pyrdm=', None,
                     "Boolean for installing PyRDM (True/False), defaults to True."),
                    ('pyrdm-path=', None, "Path to search for, or install PyRDM.")]
    install_pyrdm = None
    pyrdm_path = None

    def initialize_options(self):
        '''Set command options to default values.

        In addition to the ``setuptools.Command`` attributes, the ``InstallNonPip`` class also
        defines the attributes ``install_pyrdm`` and ``pyrdm_path``. According to ``setuptools``
        standard practice, the method ``initialize_options`` must initialise all attributes.
        Therefore, the attributes ``install_pyrdm`` and ``pyrdm_path`` are initialised in this
        method, and assigned a ``None`` value.
        '''
        self.install_pyrdm = None
        self.pyrdm_path = None

    def finalize_options(self):
        '''Set command options to final values, before running.

        The attributes ``install_pyrdm`` and ``pyrdm_path`` are set and checked by this method. The
        attributes ``install_pyrdm`` and ``pyrdm_path`` of this class should not be confused with
        the similarly named attributes of the distribution object. Packages that use
        ``setuptools-qmesh`` must scan the command line for the options ``--install-pyrdm`` and
        ``--pyrdm-path`` and pass their values to the ``setup()`` call, thus assigning the
        distribution ``install_pyrdm`` and ``pyrdm_path`` attribute values. The present method
        will then assign the distribution attribute values to the Command (present class) attribute,
        using the following procedure: If the distribution object attribute is not ``None``, its
        value is assigned to the Command object attribute. Otherwise, the ``install_pyrdm`` defaults
        to ``True`` and the ``pyrdm_path`` is given
        ``/usr/local/lib/python<version>/dist-packages/``, where <version> is obtained by the
        python used to run this setuptools method.
        '''
        import sys
        #Set the pyrdm installation location
        if self.install_pyrdm is None:
            if self.distribution.install_pyrdm is None:
                self.install_pyrdm = True
            else:
                self.install_pyrdm = self.distribution.install_pyrdm
        #Set the pyrdm installation location
        if self.pyrdm_path is None:
            if self.distribution.pyrdm_path is None:
                python_version = sys.version_info
                self.pyrdm_path = '/usr/local/lib/python'+str(python_version.major)+\
                                  '.'+str(python_version.minor)+'/dist-packages/'
            else:
                self.pyrdm_path = self.distribution.pyrdm_path

    def run(self):
        '''Method running checks for pyrdm, required to interface with setuptools.
        '''
        self.check_pyrdm()

    def check_pyrdm(self):
        '''Check if PyRDM is installed. Fetch and install if not.
        '''
        from setuptools import distutils
        import requests
        import subprocess
        try:
            import pyrdm
        except ImportError:
            self.announce(
                'Could not find PyRDM. Will Attempt to fetch from remote repository and install.',
                level=distutils.log.WARN)
            #Try downloading
            filename = 'master.tar.gz'
            url = 'https://github.com/pyrdm/pyrdm/archive/'+filename
            responce = requests.get(url, stream=True)
            if responce.ok:
                open(filename, 'wb').write(responce.content)
            else:
                msg = 'Could not fetch PyRDM repository.'
                msg += ' Responce was: ' + responce.reason
                msg += ', status code' + str(responce.status_code)
                self.announce(msg, level=distutils.log.FATAL)
                raise distutils.errors.DistutilsFileError(msg)

            #Try installing
            pyrdm_expand = subprocess.Popen(['tar', '-xzf', 'master.tar.gz'])
            pyrdm_expand.wait()
            if pyrdm_expand.returncode == 0:
                pyrdm_install = subprocess.Popen(['make', 'install'], cwd='pyrdm-master')
                pyrdm_install.wait()
                if pyrdm_install.returncode == 0:
                    pyrdm_clean = subprocess.Popen(
                        ['rm', '-rf', 'master.tar.gz', 'pyrdm-master'])
                    pyrdm_clean.wait()
                    if pyrdm_clean.returncode == 0:
                        #Try importing again, should work this time
                        import pyrdm
                        self.announce('Found PyRDM in '+pyrdm.__path__[0], level=distutils.log.INFO)
                        return
            msg = 'Could not install PyRDM.'
            self.announce(msg, level=distutils.log.FATAL)
            raise distutils.errors.DistutilsPlatformError(msg)
