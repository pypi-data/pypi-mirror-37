# -*- coding: utf-8 -*-
"""This module defines the Cython declarations related to module |anntools|.
"""

from cpython cimport PyObject

cimport numpy

cdef class ANN(object):

    cdef public numpy.int32_t nmb_inputs
    cdef public numpy.int32_t nmb_outputs
    cdef public numpy.int32_t nmb_layers
    cdef public numpy.int32_t[:] nmb_neurons
    cdef public double[:, :] weights_input
    cdef public double[:, :] weights_output
    cdef public double[:, :, :] weights_hidden
    cdef public double[:, :] intercepts_hidden
    cdef public double[:] intercepts_output
    cdef public double[:] inputs
    cdef public double[:] outputs
    cdef public double[:, :] neurons

    cpdef inline void process_actual_input(self) nogil


cdef class SeasonalANN(object):

    cdef public numpy.int32_t nmb_anns
    cdef public numpy.int32_t nmb_inputs
    cdef public numpy.int32_t nmb_outputs
    cdef PyObject **canns
    cdef public double[:, :] ratios
    cdef public double[:] inputs
    cdef public double[:] outputs

    cpdef inline void process_actual_input(self, numpy.int32_t idx_season) nogil
