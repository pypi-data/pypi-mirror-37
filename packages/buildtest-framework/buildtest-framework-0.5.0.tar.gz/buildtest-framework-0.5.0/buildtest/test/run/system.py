############################################################################
#
#  Copyright 2017-2018
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#    buildtest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    buildtest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

"""

This module will run an entire test suite for a system package. This implements
_buildtest run --system

:author: Shahzeb Siddiqui

"""

import os
import sys
from buildtest.tools.config import config_opts, BUILDTEST_SHELLTYPES
def run_system_choices():
    """
    generate choice field for _buildtest run --app
    """

    system_root_testdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],"system")
    systempkg_list = [ os.path.basename(f.path) for f in os.scandir(system_root_testdir) if f.is_dir()]

    return systempkg_list

def run_system_test(systempkg):
    """
    implementation for _buildtest run --systempkg to execute all tests in the test directory
    """

    system_root_testdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],"system")

    tests = [ f.path for f in os.scandir(os.path.join(system_root_testdir,systempkg)) if os.path.splitext(f)[1] in [".sh", ".bash", ".csh"]]

    count_test = len(tests)

    for test in tests:
        print (f"Executing Test: {test}")
        print ("---------------------------------------------------------")
        os.system(test)
        print ("---------------------------------------------------------")

    print (f"Executed {count_test} tests for system package: {systempkg}")
