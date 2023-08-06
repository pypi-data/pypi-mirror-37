#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python program that allows to extract recursively all the variables
of the Python files within a directory

This program is based on what PyLint does.
"""

from __future__ import print_function

import sys
import argparse

import inspect
from datetime import datetime
import logging

try:
    import astroid
    # from pylint.utils import PyLintASTWalker
    # from pylint.lint import PyLinter
except ImportError:
    print("eee : No module named astroid")
    print("eee : You may update pylint")
    sys.exit(1)

__docformat__ = "restructuredtext en"


class Varcounter(object):

    """
    This is the class which is used to extract the variables.

    A varnames list is initialised as empty and is filled up by the
    variable names
    """

    def __init__(self):

        """
        Initialisation of the varcounter class by setting the
        self.varnames attribute
        """

        self.varnames = []

    def extract_var(self, filein):

        """
        Function that allows to extract the variable from a file.

        An astro object that corresponds to the .py module file is initialised.

        Then, the walk function is called in this astro object
        """

        astro = astroid.MANAGER.ast_from_file(filein,
                                              filename.replace('.py', ''),
                                              source=True)
        self.walk(astro)

    def walk(self, astro):

        """
        Function that takes as an argument an astro object and that,
        for each children of the input argument, checks whether it is
        a 'variable' type object.
        If true, it appends its name on the self.varnames attribute.

        This function is recursively since it is then called with the child
        as arguments
        """

        for child in astro.get_children():
            if isinstance(child, astroid.node_classes.Name) or \
               isinstance(child, astroid.node_classes.AssName):
                self.varnames.append(child.name)

            self.walk(child)

if __name__ == '__main__':

    import os
    varcounter = Varcounter()  # initialisation of the varcounter object

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--verbose",
                        dest="is_verbose", action='store_true',
                        help="run in verbose mode.",
                        default=False)
    parser.add_argument("paths",
                        metavar='path',
                        type=str,
                        nargs='*',
                        help=("path to scan for Python files" " (default: current directory)."),
                        default=[os.getcwd()])
    parser.add_argument('--outfile',
                        metavar='output',
                        help=("output file" " (default: sys.stdout)."),
                        type=argparse.FileType('w'),
                        nargs='?',
                        default=sys.stdout)

    args = vars(parser.parse_args())

    # define log file
    command = '{0}'.format(inspect.stack()[0][3])
    log_date = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    log = '{0}/{1}.log.{2}'.format(os.environ['PROJECT_LOG'], command, log_date)
    if args['is_verbose']:
        logging.basicConfig(filename=log, level=logging.DEBUG)
    else:
        logging.basicConfig(filename=log, level=logging.INFO)

    # recursive loop over all the files within the current directory
    for root, dirs, files in os.walk(args['paths'][0]):
        for f in files:
            # if the file is a Python file
            if f.endswith('.py'):
                filename = '%s/%s' % (root, f)
                if args['is_verbose']:
                    print(filename)  # ++ log
                # we call the extract_var function on the .py file
                varcounter.extract_var(filename)

        # remove the duplication of the list
        thelist = list(set(varcounter.varnames))

    # save them to file
    for item in thelist:
        args['outfile'].write("%s\n" % item)

    args['outfile'].close()

# EXAMPLES
# ========
#
# To identify all variables of all the |pypago| Python files
#
# Assuming PAGO is in $HOME/pago_ws/ and $HOME/pago_ws/docs/manual/ is
# in your :envvar:`PATH` or :envvar:`PYTHONPATH`
#
# .. code-block:: bash
#
#    prog_var_francoise.py $HOME/pago_ws/pypago/ --outfile ginette
#
# :file:`ginette` is produced in the current directory
#
# see :ref:`typo` for usage of this file
#
# TODO
# ====
#
# rename it
#
# produce man page
#
# handle more than one path
#
# add a template of .aff file but I am not so sure of the usefulness
# until we do no add rules at least for variables
#
# may be we can plug the pylint command inside this very tool
#
# in hunspell example we need to filter the list of rst file
# to avoid scan of files generated be sphinx
#
# lunchable from anywhere
#
# make reference to other available dictionaries
#
# insensitive case alphanum sort of output
#
#
# doctest
#
# EVOLUTIONS
# ==========
#
# - fplod 20150827T155413Z guest-242.locean-ipsl.upmc.fr (Darwin)
#
#   * move usage of output to :file:`source/developers/guides/typo.rst`
#
# - fplod 20150826T113641Z guest-242.locean-ipsl.upmc.fr (Darwin)
#
#   * add parameters
#     cf. https://docs.python.org/2/library/argparse.html#module-argparse
#   * fix shebang
#
# - fplod 20150813T101137Z guest-242.locean-ipsl.upmc.fr (Darwin)
#
#   * add in example usage of the variable list in hunspell
#
# - fplod 20150813T074515Z guest-242.locean-ipsl.upmc.fr (Darwin)
#
#   * no more pep8 + pyflakes + pylint warnings
#   * save list in a file
#   * start to write an example of usage ... to be confirmed
#   * no stdout
#
# - nb 20150812
#
#   * creation
