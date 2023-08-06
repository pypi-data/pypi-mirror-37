#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compare outputs

.. warning::

   DRAFT

SYNOPSIS
========

.. code-block:: bash

   compare_outputs.py --dir1 dir1 --dir2 dir2

or

.. code-block:: bash

   compare_outputs.py --file1 file1 --file1 file2

DESCRIPTION
===========

Compare files in directories or files produced by |pago|

.. option:: --dir1 <directory>

            first directory

.. option:: --dir2 <directory>

            second directory

.. option:: --file1 <file>

            first file

.. option:: --file2 <file>

            second file


.. option:: --help
.. option:: --verbose

Start by the identification of uniq and common files.

Comparison between :file:`.mat` files uses todo hdf5

Comparison between :file:`.log` files uses  :func:`filecmp`.

Comparison between :file:`.nc` files uses  :func:`filecmp`.

Expected difference are timestamp, full path.

EXAMPLES
========

To compare directories :

.. code-block:: bash

   dir1=/home/pinsard/.pago/ciclad-ng/mapago/170/2010b/IPSL/
   dir2=/home/pinsard/.pago/ciclad-ng/mapago/170/2013b/IPSL/
   compare_outputs.py --dir1 ${dir1} --dir2 ${dir2}

Same in debug mode

.. code-block:: bash

   python -m pdb ${PAGO}/mapago/test/compare_outputs.py --dir1 ${dir1} --dir2 ${dir2}

To compare files:

.. code-block:: bash

   file1=${HOME}/.pago/sections_NA.mat
   file2=${PAGO}/mapago/test/define_sections/output/sections_NA.mat
   compare_outputs.py --file1 ${file1} --file2 ${file2}

Same in debug mode

.. code-block:: bash

   python -m pdb ${PAGO}/mapago/test/compare_outputs.py --file1 ${file1} --file2 ${file2}

For test

.. code-block:: bash

   clear; reset; python -m doctest ${PAGO}/mapago/test/compare_outputs.py

SEE ALSO
========

.. index:: tests

:ref:`rundemotest`

.. todo::

   improve synthesis

   solve useless warnings and error when

   .. code-block:: bash

      dir1=${HOME}/.pago/
      dir2=i${PAGO}/mapago/test/define_sections/output/
      compare_outputs.py --dir1 ${dir1} --dir2 ${dir2}

   after define_sections_t.m execution

   group arguments to improve usage

   improve log format

   filetype for directories parameter

   exclude subdirectories if --dir1 --dir2

   use h5py for reading mat files

   see http://stackoverflow.com/questions/874461/read-mat-files-in-python

   what about http://fr.mathworks.com/help/matlab/matlab-engine-for-python.html
"""

from __future__ import print_function

__docformat__ = "restructuredtext en"

__all__ = ['compare_filesindir',
           'compare_log',
           'compare_mat',
           'compare_nc',
           'compare_outputs', ]

import os
import sys
import argparse

import inspect
from datetime import datetime
import logging

from filecmp import dircmp
import filecmp
import difflib
import scipy.io
import numpy

# define log if send in doctest mode
logger = logging.getLogger('root')  # todo real name of the file
FORMAT = "[%(levelname)s %(pathname)s:%(lineno)d %(funcName)s]: %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


def compare_filesindir(dir1, dir2):
    """
    Compare files lists in two directories

    Identify uniq files for further investigation by operator

    Identify common files for further investigation by

    - :func:`compare_log`
    - :func:`compare_mat`
    - :func:`compare_nc`

    :param dir1 str: first directory
    :param dir2 str: second directory

    :return: list of common files
    :rtype: list

    >>> dir1 = "/home/pinsard/.pago/ciclad-ng/mapago/170/2010b/IPSL/"
    >>> print(dir1)
    /home/pinsard/.pago/ciclad-ng/mapago/170/2010b/IPSL/
    >>> dir2 = "/home/pinsard/.pago/ciclad-ng/mapago/170/2013b/IPSL/"
    >>> common_files = compare_filesindir(dir1, dir2)
    >>> common_files
    """

    logger = logging.getLogger()

    dcmp = dircmp(dir1, dir2)
    for name in dcmp.diff_files:
        logger.info("diff_file {0} found in {1} and {2}".format(name, dcmp.left, dcmp.right))

    common_files = dcmp.common_files

    if (dcmp.left_only or dcmp.right_only):
        uniq_files = dcmp.left_only + dcmp.right_only
        logger.warning("Uniq files to be checked :")
        for onefile in uniq_files:
            logger.warning("{0}".format(onefile))
    else:
        logger.info("no uniq files to be checked")

    return common_files


def compare_log(file1, file2):
    """

    compare log files ie text files

    :param file1 str: first file
    :param file2 str: second file

    :return: results of comparison
    :rtype: bool

    >>> file = 'script_PAGO_IPSL_fordev.log'
    >>> dir1="/home/pinsard/.pago/ciclad-ng/mapago/170/2013b/IPSL"
    >>> dir2="/home/pinsard/.pago/ciclad-ng/mapago/170/2010b/IPSL"
    >>> file1 = '{0}/{1}'.format(dir1, file)
    >>> file2 = '{0}/{1}'.format(dir2, file)
    >>> comparison = compare_log(file1, file2)
    >>> # comparison is false because of path differences
    >>> comparison
    False

    """

    logger = logging.getLogger()

    comparison = filecmp.cmp(file1, file2)

    if comparison:
        logger.info('files {0} and {1} are identical'.format(file1, file2))
    else:
        logger.warning('files {0} and {1} are not the same'.format(file1, file2))
        diff = difflib.ndiff(open(file1).readlines(), open(file2).readlines())
        logger.warning(''.join(diff))

    return comparison


def compare_mat(file1, file2):

    """
    compare mat files

    :param file1 str: first file
    :param file2 str: second file

    :return: results of comparison
    :rtype: bool

    >>> dir1="/home/pinsard/.pago/ciclad-ng/mapago/170/2013b/IPSL"
    >>> dir2="/home/pinsard/.pago/ciclad-ng/mapago/170/2010b/IPSL"
    >>> file="IPSLCM5_piControl2_NA_180001-184912.mat"
    >>> file1 = '{0}/{1}'.format(dir1, file)
    >>> file2 = '{0}/{1}'.format(dir2, file)
    >>> comparison = compare_mat(file1, file2)
    >>> comparison
    """
    logger = logging.getLogger()

    comparison = False  # because of timestamp

    logger.warning('matlab sequence to investigate :')
    logger.warning('matlab -r "visdiff(\'{0}\', \'{1}\')"'.format(file1, file2))

    logger.info("detailed comparison")
    mat1 = scipy.io.loadmat(file1, matlab_compatible=True)
    mat2 = scipy.io.loadmat(file2, matlab_compatible=True)

    # compare keys
    if sorted(mat1.keys()) == sorted(mat2.keys()):
        common_keys = mat1.keys()
        logger.info("same keys")
    else:
        logger.warning("files do not contains the same keys")
        logger.warning("keys in {0} : {1}".format(file1, mat1.keys()))
        logger.warning("keys in {0} : {1}".format(file2, mat2.keys()))
        # common keys
        common_keys = set(mat1.keys()) & set(mat2.keys())

    for onekey in common_keys:
        logger.info("detailed comparison on {0}".format(onekey))
        # compare types
        type1 = type(mat1[onekey])
        type2 = type(mat1[onekey])
        if not type1 == type2:
            logger.warning("different types for identical keys {0}".format(onekey))
            logger.warning("type1 : {0}".format(type1))
            logger.warning("type2 : {0}".format(type2))
            logger.warning("comparison of values not implemented")
        else:
            logger.info("same type")
            if isinstance(mat1[onekey],  numpy.ndarray):
                # if (numpy.array_equal(mat1[onekey], mat2[onekey])):
                #   logger.info("same shape same elements")
                # elif (numpy.array_equiv(mat1[onekey], mat2[onekey])):
                #   logger.info("broadcastable shape, same elements values")
                try:
                    logger.info("test for same shape, elements have close enough values")
                    numpy.allclose(mat1[onekey], mat2[onekey])
                except TypeError:
                    #     xinf = isinf(x)
                    # ++ TypeError: Not implemented for this type = pb python canopy or numpy technic
                    logger.warning("can not yet detailed difference")
                    logger.warning('matlab sequence to investigate :')
                    logger.warning('mat1 = load(\'{0}\')'.format(file1))
                    logger.warning('mat2 = load(\'{0}\')'.format(file2))
                    # ++ save de mat1 pas possible logger.warning('save(\'{0}.ascii\', \'mat1\',\'-ascii\')'.format(file1))
                    # save de mat2 pas possible logger.warning('save(\'{0}.ascii\', \'mat2\',\'-ascii\')'.format(file2))
                    # ++logger.warning('script sequence to investigate :')
                    # ++logger.warning('diff {0}.ascii {1}.ascii'.format(file1, file2))
                # ++else:
                # ++   names=mat1[onekey].dtype.names
                # ++   for name in names:
                # ++       numpy.allclose(mat1[onekey][name], mat2[onekey][name])
                # ++   logger.warning("different values of key {0} type {1} ".format(onekey, type1))
                # ++   logger.info("different values might be big ++")
            elif isinstance(mat1[onekey], str):
                if (mat1[onekey] == mat2[onekey]):
                    logger.info("same shape same value")
                else:
                    logger.warning("different values of key {0} type {1} ".format(onekey, type1))
                    logger.warning("value1 : {0}".format(mat1[onekey]))
                    logger.warning("value2 : {0}".format(mat2[onekey]))
            elif isinstance(mat1[onekey], list):
                if (mat1[onekey] == mat2[onekey]):
                    logger.info("same shape same value")
                else:
                    logger.warning("different values of key {0} type {1} ".format(onekey, type1))
                    logger.warning("value1 : {0}".format(mat1[onekey]))
                    logger.warning("value2 : {0}".format(mat2[onekey]))
            else:
                logger.warning("type {0} not yet implemented".format(type(mat1[onekey])))
                raise TypeError

    return comparison


def compare_nc(file1, file2):

    """
    compare |netcdf| files

    :param file1 str: first file
    :param file2 str: second file

    :return: results of comparison
    :rtype: bool

    >>> dir1="/home/pinsard/.pago/ciclad-ng/mapago/170/2013b/IPSL"
    >>> dir2="/home/pinsard/.pago/ciclad-ng/mapago/170/2010b/IPSL"
    >>> file="IPSLCM5_piControl2_NA_180001-184912_26n.nc"
    >>> file1 = '{0}/{1}'.format(dir1, file)
    >>> file2 = '{0}/{1}'.format(dir2, file)
    >>> comparison = compare_nc(file1, file2)
    >>> # false because of timestamp
    >>> comparison
    False

    """

    logger = logging.getLogger()

    comparison = False  # ++ because of timestamp
    if not comparison:
        logger.warning('files {0} and {1} are not the same'.format(file1, file2))

    logger.warning('script sequence to investigate :')
    logger.warning('cdo diffv {0} {1}'.format(file1, file2))

    return comparison


def compare_outputs():

    """

    main
    """
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--verbose",
                        dest="is_verbose",
                        action='store_true',
                        help="run in verbose mode.",
                        default=False)

    parser.add_argument('--dir1',
                        dest='dir1',
                        action='store',
                        metavar='<directory>',
                        help=("first directory"))

    parser.add_argument('--dir2',
                        dest='dir2',
                        action='store',
                        metavar='<directory>',
                        help=("second directory"))

    parser.add_argument('--file1',
                        dest='file1',
                        action='store',
                        metavar='<file>',
                        help=("first file"))

    parser.add_argument('--file2',
                        dest='file2',
                        action='store',
                        metavar='<file>',
                        help=("second file"))

    opts = vars(parser.parse_args())

    # define log file
    command = '{0}'.format(inspect.stack()[0][3])
    log_date = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    log = '{0}/{1}.log.{2}'.format(os.environ['PROJECT_LOG'], command, log_date)
    if opts['is_verbose']:
        logging.basicConfig(filename=log, level=logging.DEBUG)
    else:
        logging.basicConfig(filename=log, level=logging.INFO)

    logger = logging.getLogger()
    logger.info('[Context]')
    logger.info('PID={0}'.format(os.getpid()))
    logger.info('command={0}'.format(command))
    import socket
    logger.info('hostname={0}'.format(socket.getfqdn()))
    logger.info('runtime={0}'.format(log_date))
    logger.info('log={0}'.format(log))
    logger.info('[Parameters]')
    logger.info('dir1={0}'.format(opts['dir1']))
    logger.info('dir2={0}'.format(opts['dir2']))
    logger.info('file1={0}'.format(opts['file1']))
    logger.info('file2={0}'.format(opts['file2']))

    if (opts['dir1'] and opts['dir2']):
        dir1 = opts['dir1']
        dir2 = opts['dir2']
        common_files = compare_filesindir(dir1, dir2)

    if (opts['file1'] and opts['file2']):
        file1 = opts['file1']
        file2 = opts['file2']
        dir1 = os.path.dirname(opts['file1'])
        dir2 = os.path.dirname(opts['file2'])
        common_files = [file1, file2]

    files_log = [onefile for onefile in common_files if onefile.endswith('.log')]
    files_mat = [onefile for onefile in common_files if onefile.endswith('.mat')]
    files_nc = [onefile for onefile in common_files if onefile.endswith('.nc')]

    comparison = False

    # log file
    for onefile in files_log:
        file1 = '{0}/{1}'.format(dir1, onefile)
        file2 = '{0}/{1}'.format(dir2, onefile)
        comparison_log = compare_log(file1, file2)
        comparison = comparison and comparison_log

    # mat files
    for onefile in files_mat:
        if (opts['dir1'] and opts['dir2']):
            file1 = '{0}/{1}'.format(dir1, onefile)
            file2 = '{0}/{1}'.format(dir2, onefile)
        comparison_mat = compare_mat(file1, file2)
        comparison = comparison and comparison_mat

    # nc files
    for onefile in files_nc:
        file1 = '{0}/{1}'.format(dir1, onefile)
        file2 = '{0}/{1}'.format(dir2, onefile)
        comparison_nc = compare_nc(file1, file2)
        comparison = comparison and comparison_nc

    # synthesis
    logger.info("comparison : {0}".format(comparison))

# end ++

# Run main, if called from the command line
if __name__ == '__main__':
    compare_outputs()
