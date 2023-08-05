#!python
#cython: boundscheck=False
#cython: wraparound=False
#cython: initializedcheck=False
import numpy
cimport numpy
from libc.math cimport exp, fabs, log
from libc.stdio cimport *
from libc.stdlib cimport *
import cython
from cpython.mem cimport PyMem_Malloc
from cpython.mem cimport PyMem_Realloc
from cpython.mem cimport PyMem_Free
from hydpy.cythons.autogen cimport pointerutils
from hydpy.cythons.autogen cimport configutils
from hydpy.cythons.autogen cimport smoothutils
from hydpy.cythons.autogen cimport annutils

@cython.final
cdef class Parameters(object):
    cdef public ControlParameters control
    cdef public DerivedParameters derived
@cython.final
cdef class ControlParameters(object):
    cdef public double[:] xpoints
    cdef public double[:,:] ypoints
@cython.final
cdef class DerivedParameters(object):
    cdef public numpy.int32_t nmbbranches
    cdef public numpy.int32_t nmbpoints
@cython.final
cdef class Sequences(object):
    cdef public InletSequences inlets
    cdef public FluxSequences fluxes
    cdef public OutletSequences outlets
@cython.final
cdef class InletSequences(object):
    cdef double *total
    cdef public int _total_ndim
    cdef public int _total_length
    cpdef inline set_pointer0d(self, str name, pointerutils.PDouble value):
        if name == "total":
            self.total = value.p_value
@cython.final
cdef class FluxSequences(object):
    cdef public double input
    cdef public int _input_ndim
    cdef public int _input_length
    cdef public bint _input_diskflag
    cdef public str _input_path
    cdef FILE *_input_file
    cdef public bint _input_ramflag
    cdef public double[:] _input_array
    cdef public double[:] outputs
    cdef public int _outputs_ndim
    cdef public int _outputs_length
    cdef public int _outputs_length_0
    cdef public bint _outputs_diskflag
    cdef public str _outputs_path
    cdef FILE *_outputs_file
    cdef public bint _outputs_ramflag
    cdef public double[:,:] _outputs_array
    cpdef open_files(self, int idx):
        if self._input_diskflag:
            self._input_file = fopen(str(self._input_path).encode(), "rb+")
            fseek(self._input_file, idx*8, SEEK_SET)
        if self._outputs_diskflag:
            self._outputs_file = fopen(str(self._outputs_path).encode(), "rb+")
            fseek(self._outputs_file, idx*self._outputs_length*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._input_diskflag:
            fclose(self._input_file)
        if self._outputs_diskflag:
            fclose(self._outputs_file)
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._input_diskflag:
            fwrite(&self.input, 8, 1, self._input_file)
        elif self._input_ramflag:
            self._input_array[idx] = self.input
        if self._outputs_diskflag:
            fwrite(&self.outputs[0], 8, self._outputs_length, self._outputs_file)
        elif self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self._outputs_array[idx,jdx0] = self.outputs[jdx0]
@cython.final
cdef class OutletSequences(object):
    cdef double **branched
    cdef public int len_branched
    cdef public int _branched_ndim
    cdef public int _branched_length
    cdef public int _branched_length_0
    cpdef inline alloc(self, name, int length):
        if name == "branched":
            self._branched_length_0 = length
            self.branched = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc(self):
        PyMem_Free(self.branched)
    cpdef inline set_pointer1d(self, str name, pointerutils.PDouble value, int idx):
        if name == "branched":
            self.branched[idx] = value.p_value

@cython.final
cdef class Model(object):
    cdef public int idx_sim
    cdef public Parameters parameters
    cdef public Sequences sequences
    cpdef inline void doit(self, int idx)  nogil:
        self.idx_sim = idx
        self.update_inlets()
        self.run()
        self.update_outlets()
    cpdef inline void open_files(self):
        self.sequences.fluxes.open_files(self.idx_sim)
    cpdef inline void close_files(self):
        self.sequences.fluxes.close_files()
    cpdef inline void save_data(self, int idx) nogil:
        self.sequences.fluxes.save_data(self.idx_sim)
    cpdef inline void run(self) nogil:
        self.calc_outputs_v1()
    cpdef inline void update_inlets(self) nogil:
        self.pick_input_v1()
    cpdef inline void update_outlets(self) nogil:
        self.pass_outputs_v1()
    cpdef inline void update_receivers(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_senders(self, int idx) nogil:
        self.idx_sim = idx
        pass

    cpdef inline void calc_outputs_v1(self)  nogil:
        cdef int bdx
        cdef int pdx
        for pdx in range(1, self.parameters.derived.nmbpoints):
            if self.parameters.control.xpoints[pdx] > self.sequences.fluxes.input:
                break
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.fluxes.outputs[bdx] = (            (self.sequences.fluxes.input-self.parameters.control.xpoints[pdx-1]) *            (self.parameters.control.ypoints[bdx, pdx]-self.parameters.control.ypoints[bdx, pdx-1]) /            (self.parameters.control.xpoints[pdx]-self.parameters.control.xpoints[pdx-1]) +            self.parameters.control.ypoints[bdx, pdx-1])
    cpdef inline void calc_outputs(self)  nogil:
        cdef int bdx
        cdef int pdx
        for pdx in range(1, self.parameters.derived.nmbpoints):
            if self.parameters.control.xpoints[pdx] > self.sequences.fluxes.input:
                break
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.fluxes.outputs[bdx] = (            (self.sequences.fluxes.input-self.parameters.control.xpoints[pdx-1]) *            (self.parameters.control.ypoints[bdx, pdx]-self.parameters.control.ypoints[bdx, pdx-1]) /            (self.parameters.control.xpoints[pdx]-self.parameters.control.xpoints[pdx-1]) +            self.parameters.control.ypoints[bdx, pdx-1])
    cpdef inline void pick_input_v1(self)  nogil:
        self.sequences.fluxes.input = self.sequences.inlets.total[0]
    cpdef inline void pick_input(self)  nogil:
        self.sequences.fluxes.input = self.sequences.inlets.total[0]
    cpdef inline void pass_outputs_v1(self)  nogil:
        cdef int bdx
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.outlets.branched[bdx][0] = self.sequences.outlets.branched[bdx][0] + (self.sequences.fluxes.outputs[bdx])
    cpdef inline void pass_outputs(self)  nogil:
        cdef int bdx
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.outlets.branched[bdx][0] = self.sequences.outlets.branched[bdx][0] + (self.sequences.fluxes.outputs[bdx])
