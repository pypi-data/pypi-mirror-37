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
    cdef public double responses
@cython.final
cdef class DerivedParameters(object):
    cdef public numpy.int32_t nmb
    cdef public double[:] maxq
    cdef public double[:] diffq
    cdef public numpy.int32_t[:] ar_order
    cdef public numpy.int32_t[:] ma_order
    cdef public double[:,:] ar_coefs
    cdef public double[:,:] ma_coefs
@cython.final
cdef class Sequences(object):
    cdef public InletSequences inlets
    cdef public FluxSequences fluxes
    cdef public LogSequences logs
    cdef public OutletSequences outlets
@cython.final
cdef class InletSequences(object):
    cdef double **q
    cdef public int len_q
    cdef public int _q_ndim
    cdef public int _q_length
    cdef public int _q_length_0
    cpdef inline alloc(self, name, int length):
        if name == "q":
            self._q_length_0 = length
            self.q = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc(self):
        PyMem_Free(self.q)
    cpdef inline set_pointer1d(self, str name, pointerutils.PDouble value, int idx):
        if name == "q":
            self.q[idx] = value.p_value
@cython.final
cdef class FluxSequences(object):
    cdef public double qin
    cdef public int _qin_ndim
    cdef public int _qin_length
    cdef public bint _qin_diskflag
    cdef public str _qin_path
    cdef FILE *_qin_file
    cdef public bint _qin_ramflag
    cdef public double[:] _qin_array
    cdef public double[:] qpin
    cdef public int _qpin_ndim
    cdef public int _qpin_length
    cdef public int _qpin_length_0
    cdef public bint _qpin_diskflag
    cdef public str _qpin_path
    cdef FILE *_qpin_file
    cdef public bint _qpin_ramflag
    cdef public double[:,:] _qpin_array
    cdef public double[:] qma
    cdef public int _qma_ndim
    cdef public int _qma_length
    cdef public int _qma_length_0
    cdef public bint _qma_diskflag
    cdef public str _qma_path
    cdef FILE *_qma_file
    cdef public bint _qma_ramflag
    cdef public double[:,:] _qma_array
    cdef public double[:] qar
    cdef public int _qar_ndim
    cdef public int _qar_length
    cdef public int _qar_length_0
    cdef public bint _qar_diskflag
    cdef public str _qar_path
    cdef FILE *_qar_file
    cdef public bint _qar_ramflag
    cdef public double[:,:] _qar_array
    cdef public double[:] qpout
    cdef public int _qpout_ndim
    cdef public int _qpout_length
    cdef public int _qpout_length_0
    cdef public bint _qpout_diskflag
    cdef public str _qpout_path
    cdef FILE *_qpout_file
    cdef public bint _qpout_ramflag
    cdef public double[:,:] _qpout_array
    cdef public double qout
    cdef public int _qout_ndim
    cdef public int _qout_length
    cdef public bint _qout_diskflag
    cdef public str _qout_path
    cdef FILE *_qout_file
    cdef public bint _qout_ramflag
    cdef public double[:] _qout_array
    cpdef open_files(self, int idx):
        if self._qin_diskflag:
            self._qin_file = fopen(str(self._qin_path).encode(), "rb+")
            fseek(self._qin_file, idx*8, SEEK_SET)
        if self._qpin_diskflag:
            self._qpin_file = fopen(str(self._qpin_path).encode(), "rb+")
            fseek(self._qpin_file, idx*self._qpin_length*8, SEEK_SET)
        if self._qma_diskflag:
            self._qma_file = fopen(str(self._qma_path).encode(), "rb+")
            fseek(self._qma_file, idx*self._qma_length*8, SEEK_SET)
        if self._qar_diskflag:
            self._qar_file = fopen(str(self._qar_path).encode(), "rb+")
            fseek(self._qar_file, idx*self._qar_length*8, SEEK_SET)
        if self._qpout_diskflag:
            self._qpout_file = fopen(str(self._qpout_path).encode(), "rb+")
            fseek(self._qpout_file, idx*self._qpout_length*8, SEEK_SET)
        if self._qout_diskflag:
            self._qout_file = fopen(str(self._qout_path).encode(), "rb+")
            fseek(self._qout_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._qin_diskflag:
            fclose(self._qin_file)
        if self._qpin_diskflag:
            fclose(self._qpin_file)
        if self._qma_diskflag:
            fclose(self._qma_file)
        if self._qar_diskflag:
            fclose(self._qar_file)
        if self._qpout_diskflag:
            fclose(self._qpout_file)
        if self._qout_diskflag:
            fclose(self._qout_file)
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._qin_diskflag:
            fwrite(&self.qin, 8, 1, self._qin_file)
        elif self._qin_ramflag:
            self._qin_array[idx] = self.qin
        if self._qpin_diskflag:
            fwrite(&self.qpin[0], 8, self._qpin_length, self._qpin_file)
        elif self._qpin_ramflag:
            for jdx0 in range(self._qpin_length_0):
                self._qpin_array[idx,jdx0] = self.qpin[jdx0]
        if self._qma_diskflag:
            fwrite(&self.qma[0], 8, self._qma_length, self._qma_file)
        elif self._qma_ramflag:
            for jdx0 in range(self._qma_length_0):
                self._qma_array[idx,jdx0] = self.qma[jdx0]
        if self._qar_diskflag:
            fwrite(&self.qar[0], 8, self._qar_length, self._qar_file)
        elif self._qar_ramflag:
            for jdx0 in range(self._qar_length_0):
                self._qar_array[idx,jdx0] = self.qar[jdx0]
        if self._qpout_diskflag:
            fwrite(&self.qpout[0], 8, self._qpout_length, self._qpout_file)
        elif self._qpout_ramflag:
            for jdx0 in range(self._qpout_length_0):
                self._qpout_array[idx,jdx0] = self.qpout[jdx0]
        if self._qout_diskflag:
            fwrite(&self.qout, 8, 1, self._qout_file)
        elif self._qout_ramflag:
            self._qout_array[idx] = self.qout
@cython.final
cdef class LogSequences(object):
    cdef public double[:,:] login
    cdef public int _login_ndim
    cdef public int _login_length
    cdef public int _login_length_0
    cdef public int _login_length_1
    cdef public double[:,:] logout
    cdef public int _logout_ndim
    cdef public int _logout_length
    cdef public int _logout_length_0
    cdef public int _logout_length_1
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
        self.update_outlets()
    cpdef inline void open_files(self):
        self.sequences.fluxes.open_files(self.idx_sim)
    cpdef inline void close_files(self):
        self.sequences.fluxes.close_files()
    cpdef inline void save_data(self, int idx) nogil:
        self.sequences.fluxes.save_data(self.idx_sim)
    cpdef inline void run(self) nogil:
        self.calc_qpin_v1()
        self.calc_login_v1()
        self.calc_qma_v1()
        self.calc_qar_v1()
        self.calc_qpout_v1()
        self.calc_logout_v1()
        self.calc_qout_v1()
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

    cpdef inline void calc_qpin_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmb-1):
            if self.sequences.fluxes.qin < self.parameters.derived.maxq[idx]:
                self.sequences.fluxes.qpin[idx] = 0.
            elif self.sequences.fluxes.qin < self.parameters.derived.maxq[idx+1]:
                self.sequences.fluxes.qpin[idx] = self.sequences.fluxes.qin-self.parameters.derived.maxq[idx]
            else:
                self.sequences.fluxes.qpin[idx] = self.parameters.derived.diffq[idx]
        self.sequences.fluxes.qpin[self.parameters.derived.nmb-1] = max(self.sequences.fluxes.qin-self.parameters.derived.maxq[self.parameters.derived.nmb-1], 0.)
    cpdef inline void calc_login_v1(self)  nogil:
        cdef int jdx
        cdef int idx
        for idx in range(self.parameters.derived.nmb):
            for jdx in range(self.parameters.derived.ma_order[idx]-2, -1, -1):
                self.sequences.logs.login[idx, jdx+1] = self.sequences.logs.login[idx, jdx]
        for idx in range(self.parameters.derived.nmb):
            self.sequences.logs.login[idx, 0] = self.sequences.fluxes.qpin[idx]
    cpdef inline void calc_qma_v1(self)  nogil:
        cdef int jdx
        cdef int idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qma[idx] = 0.
            for jdx in range(self.parameters.derived.ma_order[idx]):
                self.sequences.fluxes.qma[idx] = self.sequences.fluxes.qma[idx] + (self.parameters.derived.ma_coefs[idx, jdx] * self.sequences.logs.login[idx, jdx])
    cpdef inline void calc_qar_v1(self)  nogil:
        cdef int jdx
        cdef int idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qar[idx] = 0.
            for jdx in range(self.parameters.derived.ar_order[idx]):
                self.sequences.fluxes.qar[idx] = self.sequences.fluxes.qar[idx] + (self.parameters.derived.ar_coefs[idx, jdx] * self.sequences.logs.logout[idx, jdx])
    cpdef inline void calc_qpout_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qpout[idx] = self.sequences.fluxes.qma[idx]+self.sequences.fluxes.qar[idx]
    cpdef inline void calc_logout_v1(self)  nogil:
        cdef int jdx
        cdef int idx
        for idx in range(self.parameters.derived.nmb):
            for jdx in range(self.parameters.derived.ar_order[idx]-2, -1, -1):
                self.sequences.logs.logout[idx, jdx+1] = self.sequences.logs.logout[idx, jdx]
        for idx in range(self.parameters.derived.nmb):
            if self.parameters.derived.ar_order[idx] > 0:
                self.sequences.logs.logout[idx, 0] = self.sequences.fluxes.qpout[idx]
    cpdef inline void calc_qout_v1(self)  nogil:
        cdef int idx
        self.sequences.fluxes.qout = 0.
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qout = self.sequences.fluxes.qout + (self.sequences.fluxes.qpout[idx])
    cpdef inline void calc_qpin(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmb-1):
            if self.sequences.fluxes.qin < self.parameters.derived.maxq[idx]:
                self.sequences.fluxes.qpin[idx] = 0.
            elif self.sequences.fluxes.qin < self.parameters.derived.maxq[idx+1]:
                self.sequences.fluxes.qpin[idx] = self.sequences.fluxes.qin-self.parameters.derived.maxq[idx]
            else:
                self.sequences.fluxes.qpin[idx] = self.parameters.derived.diffq[idx]
        self.sequences.fluxes.qpin[self.parameters.derived.nmb-1] = max(self.sequences.fluxes.qin-self.parameters.derived.maxq[self.parameters.derived.nmb-1], 0.)
    cpdef inline void calc_login(self)  nogil:
        cdef int jdx
        cdef int idx
        for idx in range(self.parameters.derived.nmb):
            for jdx in range(self.parameters.derived.ma_order[idx]-2, -1, -1):
                self.sequences.logs.login[idx, jdx+1] = self.sequences.logs.login[idx, jdx]
        for idx in range(self.parameters.derived.nmb):
            self.sequences.logs.login[idx, 0] = self.sequences.fluxes.qpin[idx]
    cpdef inline void calc_qma(self)  nogil:
        cdef int jdx
        cdef int idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qma[idx] = 0.
            for jdx in range(self.parameters.derived.ma_order[idx]):
                self.sequences.fluxes.qma[idx] = self.sequences.fluxes.qma[idx] + (self.parameters.derived.ma_coefs[idx, jdx] * self.sequences.logs.login[idx, jdx])
    cpdef inline void calc_qar(self)  nogil:
        cdef int jdx
        cdef int idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qar[idx] = 0.
            for jdx in range(self.parameters.derived.ar_order[idx]):
                self.sequences.fluxes.qar[idx] = self.sequences.fluxes.qar[idx] + (self.parameters.derived.ar_coefs[idx, jdx] * self.sequences.logs.logout[idx, jdx])
    cpdef inline void calc_qpout(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qpout[idx] = self.sequences.fluxes.qma[idx]+self.sequences.fluxes.qar[idx]
    cpdef inline void calc_logout(self)  nogil:
        cdef int jdx
        cdef int idx
        for idx in range(self.parameters.derived.nmb):
            for jdx in range(self.parameters.derived.ar_order[idx]-2, -1, -1):
                self.sequences.logs.logout[idx, jdx+1] = self.sequences.logs.logout[idx, jdx]
        for idx in range(self.parameters.derived.nmb):
            if self.parameters.derived.ar_order[idx] > 0:
                self.sequences.logs.logout[idx, 0] = self.sequences.fluxes.qpout[idx]
    cpdef inline void calc_qout(self)  nogil:
        cdef int idx
        self.sequences.fluxes.qout = 0.
        for idx in range(self.parameters.derived.nmb):
            self.sequences.fluxes.qout = self.sequences.fluxes.qout + (self.sequences.fluxes.qpout[idx])
    cpdef inline void pick_q_v1(self)  nogil:
        cdef int idx
        self.sequences.fluxes.qin = 0.
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qin = self.sequences.fluxes.qin + (self.sequences.inlets.q[idx][0])
    cpdef inline void pick_q(self)  nogil:
        cdef int idx
        self.sequences.fluxes.qin = 0.
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qin = self.sequences.fluxes.qin + (self.sequences.inlets.q[idx][0])
    cpdef inline void pass_q_v1(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.qout)
    cpdef inline void pass_q(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.qout)
