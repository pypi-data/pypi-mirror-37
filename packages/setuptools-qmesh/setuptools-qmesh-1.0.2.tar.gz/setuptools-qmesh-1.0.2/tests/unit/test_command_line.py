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
'''Module containing tests of setuptools-qmesh command line options.

This module tests that all command line options introduced by setuptools-qmesh
complete, with a zero-code returned.
'''

import unittest

class TestCommandLineExtensions(unittest.TestCase):
    '''Test class for setuptools-qmesh command line extensions.

    Class (derived from unittest.TestCase) testing that all command line
    options introduced by setuptools-qmesh complete, with a zero-code returned.
    '''

    def setUp(self):
        '''Method setting-up test environment.

        This method is *not* intended to be invoked by the user. It stores the
        path of the testing function, the project root path (setuptools-qmesh)
        and the path of the command configuration file.
        '''
        import os
        import sys
        import logging
        #Create logger object
        self.log = logging.log
        #Construct absolute paths to test directory and project root directory
        self.this_path = os.path.dirname(os.path.realpath(__file__))
        self.project_test_path = os.path.split(self.this_path)[0]
        self.project_root_path = os.path.split(self.project_test_path)[0]
        #Detect python version used to run test, as a string in the
        # form 'major.minor'
        python_version_info = sys.version_info
        self.python_version = str(python_version_info.major) + \
                              '.' + str(python_version_info.minor)

    def test_help_commands(self):
        '''Method testing the setup.py script with the --help-commands option.
        '''
        import os
        #Construct path to the setup.py script
        setup_script_path = os.path.join(self.project_root_path, 'setup.py')
        #Assemble string of command to test
        command = ['python' + self.python_version, setup_script_path, '--help-commands']
        #Invoke command on setup.py script
        self.invoke_and_test_command(command)

    def invoke_and_test_command(self, command):
        '''Method invoking setuptools commands and checking return codes.

        The setuptools commands are issued using the Python version that
        runs the test.
        '''
        import tempfile
        import subprocess
        #Invoke command and capture stdout & stderr to temporary files
        command_stdout = tempfile.TemporaryFile(mode='w+b')
        command_stderr = tempfile.TemporaryFile(mode='w+b')
        command_proc = subprocess.Popen(command,
                                        stdout=command_stdout,
                                        stderr=command_stderr)
        command_proc.wait()
        #If command had issues, echo its stdout and stdout
        if command_proc.returncode != 0:
            command_stdout.seek(0)
            self.log(40, '***command stdout:')
            for line in command_stdout:
                self.log(40, line.decode('utf-8').strip('\n'))
            command_stderr.seek(0)
            self.log(40, '***command stderr:')
            for line in command_stderr:
                self.log(40, line.decode('utf-8').strip('\n'))
        #Close files
        command_stdout.close()
        command_stderr.close()
        #Make sure command has run without issues
        self.assertEqual(command_proc.returncode, 0,
                         'The command '+ ' '.join(command) +\
                         ' returned a non-zero code: '+str(command_proc.returncode)+'.'+\
                         ' Please check command output.')
