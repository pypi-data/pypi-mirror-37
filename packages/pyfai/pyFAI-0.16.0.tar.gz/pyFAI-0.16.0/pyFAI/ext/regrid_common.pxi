# coding: utf-8
#
#    Project: Azimuthal integration
#             https://github.com/silx-kit/pyFAI
#
#    Copyright (C) 2015-2018 European Synchrotron Radiation Facility, Grenoble, France
#
#    Principal author:       Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Common cdef constants and functions for preprocessing"""

__author__ = "Jerome Kieffer"
__contact__ = "Jerome.kieffer@esrf.fr"
__date__ = "17/07/2018"
__status__ = "stable"
__license__ = "MIT"

include "numpy_common.pxi"
import cython
cimport numpy
import numpy
from cython cimport floating
from libc.math cimport fabs, M_PI

# How position are stored
ctypedef numpy.float64_t position_t
position_d = numpy.float64

# How weights or data are stored 
ctypedef numpy.float32_t data_t
data_d = numpy.float32

# how data are accumulated 
ctypedef numpy.float64_t acc_t
acc_d = numpy.float64

# type of the mask:
ctypedef numpy.int8_t mask_t
mask_d = numpy.int8


cdef:
    float pi = <float> M_PI
    float piover2 = <float> (pi * 0.5)
    float onef = <float> 1.0
    float zerof = <float> 1.0
    double EPS32 = (1.0 + numpy.finfo(numpy.float32).eps)


@cython.cdivision(True)
cdef inline floating  get_bin_number(floating x0, floating pos0_min, floating delta) nogil:
    """
    calculate the bin number for any point (as floating)

    :param x0: current position
    :param pos0_min: position minimum
    :param delta: bin width
    :return: bin number as floating point.
    """
    return (x0 - pos0_min) / delta


@cython.cdivision(True)
cdef inline floating calc_upper_bound(floating maximum_value) nogil:
    """Calculate the upper_bound for an histogram, 
    given the maximum value of all the data.
    
    :param maximum_value: maximum value over all elements
    :return: the smallest 32 bit float greater than the maximum
    """
    if maximum_value > 0:
        return maximum_value * EPS32
    else:
        return maximum_value / EPS32
