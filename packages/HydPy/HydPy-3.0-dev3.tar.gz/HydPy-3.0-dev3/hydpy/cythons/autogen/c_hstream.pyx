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
    cdef public double lag
    cdef public double damp
@cython.final
cdef class DerivedParameters(object):
    cdef public numpy.int32_t nmbsegments
    cdef public double c1
    cdef public double c3
    cdef public double c2
@cython.final
cdef class Sequences(object):
    cdef public InletSequences inlets
    cdef public StateSequences states
    cdef public OutletSequences outlets
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InletSequences(object):
    cdef double *q
    cdef public int _q_ndim
    cdef public int _q_length
    cpdef inline set_pointer0d(self, str name, pointerutils.PDouble value):
        if name == "q":
            self.q = value.p_value
@cython.final
cdef class StateSequences(object):
    cdef public double[:] qjoints
    cdef public int _qjoints_ndim
    cdef public int _qjoints_length
    cdef public int _qjoints_length_0
    cdef public bint _qjoints_diskflag
    cdef public str _qjoints_path
    cdef FILE *_qjoints_file
    cdef public bint _qjoints_ramflag
    cdef public double[:,:] _qjoints_array
    cpdef open_files(self, int idx):
        if self._qjoints_diskflag:
            self._qjoints_file = fopen(str(self._qjoints_path).encode(), "rb+")
            fseek(self._qjoints_file, idx*self._qjoints_length*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._qjoints_diskflag:
            fclose(self._qjoints_file)
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._qjoints_diskflag:
            fwrite(&self.qjoints[0], 8, self._qjoints_length, self._qjoints_file)
        elif self._qjoints_ramflag:
            for jdx0 in range(self._qjoints_length_0):
                self._qjoints_array[idx,jdx0] = self.qjoints[jdx0]
@cython.final
cdef class OutletSequences(object):
    cdef double *q
    cdef public int _q_ndim
    cdef public int _q_length
    cpdef inline set_pointer0d(self, str name, pointerutils.PDouble value):
        if name == "q":
            self.q = value.p_value

@cython.final
cdef class Model(object):
    cdef public int idx_sim
    cdef public Parameters parameters
    cdef public Sequences sequences
    cpdef inline void doit(self, int idx)  nogil:
        self.idx_sim = idx
        self.update_inlets()
        self.run()
        self.new2old()
        self.update_outlets()
    cpdef inline void open_files(self):
        self.sequences.states.open_files(self.idx_sim)
    cpdef inline void close_files(self):
        self.sequences.states.close_files()
    cpdef inline void save_data(self, int idx) nogil:
        self.sequences.states.save_data(self.idx_sim)
    cpdef inline void new2old(self) nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        for jdx0 in range(self.sequences.states._qjoints_length_0):
            self.sequences.old_states.qjoints[jdx0] = self.sequences.new_states.qjoints[jdx0]
    cpdef inline void run(self) nogil:
        self.calc_qjoints_v1()
    cpdef inline void update_inlets(self) nogil:
        self.pick_q_v1()
    cpdef inline void update_outlets(self) nogil:
        self.pass_q_v1()
    cpdef inline void update_receivers(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_senders(self, int idx) nogil:
        self.idx_sim = idx
        pass

    cpdef inline void calc_qjoints_v1(self)  nogil:
        cdef int j
        for j in range(self.parameters.derived.nmbsegments):
            self.sequences.new_states.qjoints[j+1] = (self.parameters.derived.c1*self.sequences.new_states.qjoints[j] +                            self.parameters.derived.c2*self.sequences.old_states.qjoints[j] +                            self.parameters.derived.c3*self.sequences.old_states.qjoints[j+1])
    cpdef inline void calc_qjoints(self)  nogil:
        cdef int j
        for j in range(self.parameters.derived.nmbsegments):
            self.sequences.new_states.qjoints[j+1] = (self.parameters.derived.c1*self.sequences.new_states.qjoints[j] +                            self.parameters.derived.c2*self.sequences.old_states.qjoints[j] +                            self.parameters.derived.c3*self.sequences.old_states.qjoints[j+1])
    cpdef inline void pick_q_v1(self)  nogil:
        self.sequences.states.qjoints[0] = self.sequences.inlets.q[0]
    cpdef inline void pick_q(self)  nogil:
        self.sequences.states.qjoints[0] = self.sequences.inlets.q[0]
    cpdef inline void pass_q_v1(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.states.qjoints[self.parameters.derived.nmbsegments])
    cpdef inline void pass_q(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.states.qjoints[self.parameters.derived.nmbsegments])
