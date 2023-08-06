#!/usr/bin/env python

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
'''Module containing tests towards PEP8 compliance.

The pylint utility is used to check for PEP8 compliance. The file pylint.cfg
contains the configuration options for pylint, and it also points to spell checks
and spelling exceptions.
'''

import unittest

class TestPEP8(unittest.TestCase):
    '''Class for PEP8 compliance of setuptools-qmesh.

    Class (derived from unittest.TestCase) for PEP8 compliance testing.
    '''

    def setUp(self):
        '''Method setting-up test environment.

        This method is not aimed to be invoked by the user. It stores the path of
        the testing function, the project root path (setuptools-qmesh) and the
        path of the pylint configuration file.
        '''
        import os
        #Create logger object
        import logging
        self.log = logging.log
        #Construct absolute paths to test directory and project root directory
        self.this_path = os.path.dirname(os.path.realpath(__file__))
        self.project_test_path = os.path.split(self.this_path)[0]
        self.project_root_path = os.path.split(self.project_test_path)[0]
        #Store the path to the local pylint configuration file
        self.pylint_rcfile = os.path.join(self.this_path, 'pylint.cfg')

    def test_setup_script(self):
        '''Method testing the setup.py script, in setuptools-qmesh, for PEP8 compliance.
        '''
        import os
        #Construct path to the setup.py script
        setup_script_path = os.path.join(self.project_root_path, 'setup.py')
        #Invoke pylint on setup.py script
        self.invoke_pylint(setup_script_path)

    def test_setuptools_qmesh(self):
        '''Method testing setuptools-qmesh for PEP8 compliance.
        '''
        import os
        #Construct path to the setuptools_qmesh script
        setuptools_qmesh_path = os.path.join(self.project_root_path, 'setuptools_qmesh')
        #Invoke pylint on setuptools_qmesh package.
        self.invoke_pylint(setuptools_qmesh_path)

    def test_the_tests(self):
        '''Self-check: Method assessing the test code for PEP8 compliance.
        '''
        #Invoke pylint on this file.
        self.invoke_pylint(self.project_test_path)

    def invoke_pylint(self, file_or_path):
        '''Method facilitating pylint invocation.
        '''
        import tempfile
        import subprocess
        #Invoke pylint and capture pylint stdout & stderr to temporary files
        pylint_command = ['pylint', '--rcfile', self.pylint_rcfile, file_or_path]
        pylint_stdout = tempfile.TemporaryFile(mode='w+b')
        pylint_stderr = tempfile.TemporaryFile(mode='w+b')
        pylint_proc = subprocess.Popen(pylint_command, stdout=pylint_stdout, stderr=pylint_stderr)
        pylint_proc.wait()
        #If pylint had issues, echo its stdout and stdout
        if pylint_proc.returncode != 0:
            pylint_stdout.seek(0)
            self.log(40, '***pylint stdout:')
            for line in pylint_stdout:
                self.log(40, line.decode('utf-8').strip('\n'))
            pylint_stderr.seek(0)
            self.log(40, '***pylint stderr:')
            for line in pylint_stderr:
                self.log(40, line.decode('utf-8').strip('\n'))
        #Close files
        pylint_stdout.close()
        pylint_stderr.close()
        #Make sure pylint has run without issues
        self.assertEqual(pylint_proc.returncode, 0,
                         'pylint returned a non-zero code: '+str(pylint_proc.returncode)+'.'+\
                         ' Please check pylint output.')

if __name__ == '__main__':
    unittest.main()
