#!/usr/bin/env python
############################################################################
#
#  Copyright 2017-2018
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#    This file is part of buildtest.
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
Methods for list subcommand

:author: Shahzeb Siddiqui (Pfizer)
"""
import json
import sys

from buildtest.tools.easybuild import get_toolchains, find_easyconfigs
from buildtest.tools.print_functions import print_software, print_toolchain, print_software_version_relation, print_software_version_relation_csv
from buildtest.tools.software import get_unique_software, software_version_relation

def func_list_subcmd(args):
    """ entry method for list subcommand"""

    if args.easyconfigs:
        find_easyconfigs()
    elif args.list_toolchain:
        list_toolchain(args)
    elif args.list_unique_software:
        list_software(args)
    elif args.software_version_relation:
        list_software_version_relation(args)

    sys.exit(0)

def list_toolchain(args):
    """ implementation for  "_buildtest list -lt" """
    toolchain_set=get_toolchains()
    if args.format == "stdout":
        print_toolchain(toolchain_set)
    elif args.format == "json":
        json.dump(toolchain_set, sys.stdout, indent=4, sort_keys=True)


def list_software(args):
    """ implementation for  "_buildtest list -ls" """
    software_set=get_unique_software()

    if args.format == "stdout":
        print_software(software_set)
    elif args.format == "json":
        json.dump(software_set, sys.stdout, indent=4, sort_keys=True)


def list_software_version_relation(args):
    """ implementation for  "_buildtest list -svr" """
    software_dict = software_version_relation()

    if args.format == "stdout":
        print_software_version_relation(software_dict)
    elif args.format == "csv":
        print_software_version_relation_csv(software_dict)

    sys.exit(0)
