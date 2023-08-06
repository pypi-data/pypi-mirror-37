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
    cdef public double laen
    cdef public double gef
    cdef public double hm
    cdef public double bm
    cdef public double[:] bv
    cdef public double[:] bbv
    cdef public double bnm
    cdef public double[:] bnv
    cdef public double[:] bnvr
    cdef public double skm
    cdef public double[:] skv
    cdef public double ekm
    cdef public double[:] ekv
    cdef public double qtol
    cdef public double htol
@cython.final
cdef class DerivedParameters(object):
    cdef public double[:] hv
    cdef public double qm
    cdef public double[:] qv
    cdef public double sek
@cython.final
cdef class Sequences(object):
    cdef public InletSequences inlets
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public AideSequences aides
    cdef public OutletSequences outlets
    cdef public StateSequences old_states
    cdef public StateSequences new_states
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
    cdef public double qref
    cdef public int _qref_ndim
    cdef public int _qref_length
    cdef public bint _qref_diskflag
    cdef public str _qref_path
    cdef FILE *_qref_file
    cdef public bint _qref_ramflag
    cdef public double[:] _qref_array
    cdef public double h
    cdef public int _h_ndim
    cdef public int _h_length
    cdef public bint _h_diskflag
    cdef public str _h_path
    cdef FILE *_h_file
    cdef public bint _h_ramflag
    cdef public double[:] _h_array
    cdef public double am
    cdef public int _am_ndim
    cdef public int _am_length
    cdef public bint _am_diskflag
    cdef public str _am_path
    cdef FILE *_am_file
    cdef public bint _am_ramflag
    cdef public double[:] _am_array
    cdef public double[:] av
    cdef public int _av_ndim
    cdef public int _av_length
    cdef public int _av_length_0
    cdef public bint _av_diskflag
    cdef public str _av_path
    cdef FILE *_av_file
    cdef public bint _av_ramflag
    cdef public double[:,:] _av_array
    cdef public double[:] avr
    cdef public int _avr_ndim
    cdef public int _avr_length
    cdef public int _avr_length_0
    cdef public bint _avr_diskflag
    cdef public str _avr_path
    cdef FILE *_avr_file
    cdef public bint _avr_ramflag
    cdef public double[:,:] _avr_array
    cdef public double ag
    cdef public int _ag_ndim
    cdef public int _ag_length
    cdef public bint _ag_diskflag
    cdef public str _ag_path
    cdef FILE *_ag_file
    cdef public bint _ag_ramflag
    cdef public double[:] _ag_array
    cdef public double um
    cdef public int _um_ndim
    cdef public int _um_length
    cdef public bint _um_diskflag
    cdef public str _um_path
    cdef FILE *_um_file
    cdef public bint _um_ramflag
    cdef public double[:] _um_array
    cdef public double[:] uv
    cdef public int _uv_ndim
    cdef public int _uv_length
    cdef public int _uv_length_0
    cdef public bint _uv_diskflag
    cdef public str _uv_path
    cdef FILE *_uv_file
    cdef public bint _uv_ramflag
    cdef public double[:,:] _uv_array
    cdef public double[:] uvr
    cdef public int _uvr_ndim
    cdef public int _uvr_length
    cdef public int _uvr_length_0
    cdef public bint _uvr_diskflag
    cdef public str _uvr_path
    cdef FILE *_uvr_file
    cdef public bint _uvr_ramflag
    cdef public double[:,:] _uvr_array
    cdef public double qm
    cdef public int _qm_ndim
    cdef public int _qm_length
    cdef public bint _qm_diskflag
    cdef public str _qm_path
    cdef FILE *_qm_file
    cdef public bint _qm_ramflag
    cdef public double[:] _qm_array
    cdef public double[:] qv
    cdef public int _qv_ndim
    cdef public int _qv_length
    cdef public int _qv_length_0
    cdef public bint _qv_diskflag
    cdef public str _qv_path
    cdef FILE *_qv_file
    cdef public bint _qv_ramflag
    cdef public double[:,:] _qv_array
    cdef public double[:] qvr
    cdef public int _qvr_ndim
    cdef public int _qvr_length
    cdef public int _qvr_length_0
    cdef public bint _qvr_diskflag
    cdef public str _qvr_path
    cdef FILE *_qvr_file
    cdef public bint _qvr_ramflag
    cdef public double[:,:] _qvr_array
    cdef public double qg
    cdef public int _qg_ndim
    cdef public int _qg_length
    cdef public bint _qg_diskflag
    cdef public str _qg_path
    cdef FILE *_qg_file
    cdef public bint _qg_ramflag
    cdef public double[:] _qg_array
    cdef public double rk
    cdef public int _rk_ndim
    cdef public int _rk_length
    cdef public bint _rk_diskflag
    cdef public str _rk_path
    cdef FILE *_rk_file
    cdef public bint _rk_ramflag
    cdef public double[:] _rk_array
    cpdef open_files(self, int idx):
        if self._qref_diskflag:
            self._qref_file = fopen(str(self._qref_path).encode(), "rb+")
            fseek(self._qref_file, idx*8, SEEK_SET)
        if self._h_diskflag:
            self._h_file = fopen(str(self._h_path).encode(), "rb+")
            fseek(self._h_file, idx*8, SEEK_SET)
        if self._am_diskflag:
            self._am_file = fopen(str(self._am_path).encode(), "rb+")
            fseek(self._am_file, idx*8, SEEK_SET)
        if self._av_diskflag:
            self._av_file = fopen(str(self._av_path).encode(), "rb+")
            fseek(self._av_file, idx*self._av_length*8, SEEK_SET)
        if self._avr_diskflag:
            self._avr_file = fopen(str(self._avr_path).encode(), "rb+")
            fseek(self._avr_file, idx*self._avr_length*8, SEEK_SET)
        if self._ag_diskflag:
            self._ag_file = fopen(str(self._ag_path).encode(), "rb+")
            fseek(self._ag_file, idx*8, SEEK_SET)
        if self._um_diskflag:
            self._um_file = fopen(str(self._um_path).encode(), "rb+")
            fseek(self._um_file, idx*8, SEEK_SET)
        if self._uv_diskflag:
            self._uv_file = fopen(str(self._uv_path).encode(), "rb+")
            fseek(self._uv_file, idx*self._uv_length*8, SEEK_SET)
        if self._uvr_diskflag:
            self._uvr_file = fopen(str(self._uvr_path).encode(), "rb+")
            fseek(self._uvr_file, idx*self._uvr_length*8, SEEK_SET)
        if self._qm_diskflag:
            self._qm_file = fopen(str(self._qm_path).encode(), "rb+")
            fseek(self._qm_file, idx*8, SEEK_SET)
        if self._qv_diskflag:
            self._qv_file = fopen(str(self._qv_path).encode(), "rb+")
            fseek(self._qv_file, idx*self._qv_length*8, SEEK_SET)
        if self._qvr_diskflag:
            self._qvr_file = fopen(str(self._qvr_path).encode(), "rb+")
            fseek(self._qvr_file, idx*self._qvr_length*8, SEEK_SET)
        if self._qg_diskflag:
            self._qg_file = fopen(str(self._qg_path).encode(), "rb+")
            fseek(self._qg_file, idx*8, SEEK_SET)
        if self._rk_diskflag:
            self._rk_file = fopen(str(self._rk_path).encode(), "rb+")
            fseek(self._rk_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._qref_diskflag:
            fclose(self._qref_file)
        if self._h_diskflag:
            fclose(self._h_file)
        if self._am_diskflag:
            fclose(self._am_file)
        if self._av_diskflag:
            fclose(self._av_file)
        if self._avr_diskflag:
            fclose(self._avr_file)
        if self._ag_diskflag:
            fclose(self._ag_file)
        if self._um_diskflag:
            fclose(self._um_file)
        if self._uv_diskflag:
            fclose(self._uv_file)
        if self._uvr_diskflag:
            fclose(self._uvr_file)
        if self._qm_diskflag:
            fclose(self._qm_file)
        if self._qv_diskflag:
            fclose(self._qv_file)
        if self._qvr_diskflag:
            fclose(self._qvr_file)
        if self._qg_diskflag:
            fclose(self._qg_file)
        if self._rk_diskflag:
            fclose(self._rk_file)
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._qref_diskflag:
            fwrite(&self.qref, 8, 1, self._qref_file)
        elif self._qref_ramflag:
            self._qref_array[idx] = self.qref
        if self._h_diskflag:
            fwrite(&self.h, 8, 1, self._h_file)
        elif self._h_ramflag:
            self._h_array[idx] = self.h
        if self._am_diskflag:
            fwrite(&self.am, 8, 1, self._am_file)
        elif self._am_ramflag:
            self._am_array[idx] = self.am
        if self._av_diskflag:
            fwrite(&self.av[0], 8, self._av_length, self._av_file)
        elif self._av_ramflag:
            for jdx0 in range(self._av_length_0):
                self._av_array[idx,jdx0] = self.av[jdx0]
        if self._avr_diskflag:
            fwrite(&self.avr[0], 8, self._avr_length, self._avr_file)
        elif self._avr_ramflag:
            for jdx0 in range(self._avr_length_0):
                self._avr_array[idx,jdx0] = self.avr[jdx0]
        if self._ag_diskflag:
            fwrite(&self.ag, 8, 1, self._ag_file)
        elif self._ag_ramflag:
            self._ag_array[idx] = self.ag
        if self._um_diskflag:
            fwrite(&self.um, 8, 1, self._um_file)
        elif self._um_ramflag:
            self._um_array[idx] = self.um
        if self._uv_diskflag:
            fwrite(&self.uv[0], 8, self._uv_length, self._uv_file)
        elif self._uv_ramflag:
            for jdx0 in range(self._uv_length_0):
                self._uv_array[idx,jdx0] = self.uv[jdx0]
        if self._uvr_diskflag:
            fwrite(&self.uvr[0], 8, self._uvr_length, self._uvr_file)
        elif self._uvr_ramflag:
            for jdx0 in range(self._uvr_length_0):
                self._uvr_array[idx,jdx0] = self.uvr[jdx0]
        if self._qm_diskflag:
            fwrite(&self.qm, 8, 1, self._qm_file)
        elif self._qm_ramflag:
            self._qm_array[idx] = self.qm
        if self._qv_diskflag:
            fwrite(&self.qv[0], 8, self._qv_length, self._qv_file)
        elif self._qv_ramflag:
            for jdx0 in range(self._qv_length_0):
                self._qv_array[idx,jdx0] = self.qv[jdx0]
        if self._qvr_diskflag:
            fwrite(&self.qvr[0], 8, self._qvr_length, self._qvr_file)
        elif self._qvr_ramflag:
            for jdx0 in range(self._qvr_length_0):
                self._qvr_array[idx,jdx0] = self.qvr[jdx0]
        if self._qg_diskflag:
            fwrite(&self.qg, 8, 1, self._qg_file)
        elif self._qg_ramflag:
            self._qg_array[idx] = self.qg
        if self._rk_diskflag:
            fwrite(&self.rk, 8, 1, self._rk_file)
        elif self._rk_ramflag:
            self._rk_array[idx] = self.rk
@cython.final
cdef class StateSequences(object):
    cdef public double qz
    cdef public int _qz_ndim
    cdef public int _qz_length
    cdef public bint _qz_diskflag
    cdef public str _qz_path
    cdef FILE *_qz_file
    cdef public bint _qz_ramflag
    cdef public double[:] _qz_array
    cdef public double qa
    cdef public int _qa_ndim
    cdef public int _qa_length
    cdef public bint _qa_diskflag
    cdef public str _qa_path
    cdef FILE *_qa_file
    cdef public bint _qa_ramflag
    cdef public double[:] _qa_array
    cpdef open_files(self, int idx):
        if self._qz_diskflag:
            self._qz_file = fopen(str(self._qz_path).encode(), "rb+")
            fseek(self._qz_file, idx*8, SEEK_SET)
        if self._qa_diskflag:
            self._qa_file = fopen(str(self._qa_path).encode(), "rb+")
            fseek(self._qa_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._qz_diskflag:
            fclose(self._qz_file)
        if self._qa_diskflag:
            fclose(self._qa_file)
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._qz_diskflag:
            fwrite(&self.qz, 8, 1, self._qz_file)
        elif self._qz_ramflag:
            self._qz_array[idx] = self.qz
        if self._qa_diskflag:
            fwrite(&self.qa, 8, 1, self._qa_file)
        elif self._qa_ramflag:
            self._qa_array[idx] = self.qa
@cython.final
cdef class AideSequences(object):
    cdef public double temp
    cdef public int _temp_ndim
    cdef public int _temp_length
    cdef public double hmin
    cdef public int _hmin_ndim
    cdef public int _hmin_length
    cdef public double hmax
    cdef public int _hmax_ndim
    cdef public int _hmax_length
    cdef public double qmin
    cdef public int _qmin_ndim
    cdef public int _qmin_length
    cdef public double qmax
    cdef public int _qmax_ndim
    cdef public int _qmax_length
    cdef public double qtest
    cdef public int _qtest_ndim
    cdef public int _qtest_length
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
        self.sequences.fluxes.open_files(self.idx_sim)
        self.sequences.states.open_files(self.idx_sim)
    cpdef inline void close_files(self):
        self.sequences.fluxes.close_files()
        self.sequences.states.close_files()
    cpdef inline void save_data(self, int idx) nogil:
        self.sequences.fluxes.save_data(self.idx_sim)
        self.sequences.states.save_data(self.idx_sim)
    cpdef inline void new2old(self) nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        self.sequences.old_states.qz = self.sequences.new_states.qz
        self.sequences.old_states.qa = self.sequences.new_states.qa
    cpdef inline void run(self) nogil:
        self.calc_qref_v1()
        self.calc_hmin_qmin_hmax_qmax_v1()
        self.calc_h_v1()
        self.calc_ag_v1()
        self.calc_rk_v1()
        self.calc_qa_v1()
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

    cpdef inline void calc_qref_v1(self)  nogil:
        self.sequences.fluxes.qref = (self.sequences.new_states.qz+self.sequences.old_states.qz+self.sequences.old_states.qa)/3.
    cpdef inline void calc_hmin_qmin_hmax_qmax_v1(self)  nogil:
        if self.sequences.fluxes.qref <= self.parameters.derived.qm:
            self.sequences.aides.hmin = 0.
            self.sequences.aides.qmin = 0.
            self.sequences.aides.hmax = self.parameters.control.hm
            self.sequences.aides.qmax = self.parameters.derived.qm
        elif self.sequences.fluxes.qref <= min(self.parameters.derived.qv[0], self.parameters.derived.qv[1]):
            self.sequences.aides.hmin = self.parameters.control.hm
            self.sequences.aides.qmin = self.parameters.derived.qm
            self.sequences.aides.hmax = self.parameters.control.hm+min(self.parameters.derived.hv[0], self.parameters.derived.hv[1])
            self.sequences.aides.qmax = min(self.parameters.derived.qv[0], self.parameters.derived.qv[1])
        elif self.sequences.fluxes.qref < max(self.parameters.derived.qv[0], self.parameters.derived.qv[1]):
            self.sequences.aides.hmin = self.parameters.control.hm+min(self.parameters.derived.hv[0], self.parameters.derived.hv[1])
            self.sequences.aides.qmin = min(self.parameters.derived.qv[0], self.parameters.derived.qv[1])
            self.sequences.aides.hmax = self.parameters.control.hm+max(self.parameters.derived.hv[0], self.parameters.derived.hv[1])
            self.sequences.aides.qmax = max(self.parameters.derived.qv[0], self.parameters.derived.qv[1])
        else:
            self.sequences.fluxes.h = self.parameters.control.hm+max(self.parameters.derived.hv[0], self.parameters.derived.hv[1])
            self.sequences.aides.hmin = self.sequences.fluxes.h
            self.sequences.aides.qmin = self.sequences.fluxes.qg
            while True:
                self.sequences.fluxes.h = self.sequences.fluxes.h * (2.)
                self.calc_qg()
                if self.sequences.fluxes.qg < self.sequences.fluxes.qref:
                    self.sequences.aides.hmin = self.sequences.fluxes.h
                    self.sequences.aides.qmin = self.sequences.fluxes.qg
                else:
                    self.sequences.aides.hmax = self.sequences.fluxes.h
                    self.sequences.aides.qmax = self.sequences.fluxes.qg
                    break
    cpdef inline void calc_h_v1(self)  nogil:
        self.sequences.aides.qmin = self.sequences.aides.qmin - (self.sequences.fluxes.qref)
        self.sequences.aides.qmax = self.sequences.aides.qmax - (self.sequences.fluxes.qref)
        if fabs(self.sequences.aides.qmin) < self.parameters.control.qtol:
            self.sequences.fluxes.h = self.sequences.aides.hmin
            self.calc_qg()
        elif fabs(self.sequences.aides.qmax) < self.parameters.control.qtol:
            self.sequences.fluxes.h = self.sequences.aides.hmax
            self.calc_qg()
        elif fabs(self.sequences.aides.hmax-self.sequences.aides.hmin) < self.parameters.control.htol:
            self.sequences.fluxes.h = (self.sequences.aides.hmin+self.sequences.aides.hmax)/2.
            self.calc_qg()
        else:
            while True:
                self.sequences.fluxes.h = self.sequences.aides.hmin-self.sequences.aides.qmin*(self.sequences.aides.hmax-self.sequences.aides.hmin)/(self.sequences.aides.qmax-self.sequences.aides.qmin)
                self.calc_qg()
                self.sequences.aides.qtest = self.sequences.fluxes.qg-self.sequences.fluxes.qref
                if fabs(self.sequences.aides.qtest) < self.parameters.control.qtol:
                    return
                elif (((self.sequences.aides.qmax < 0.) and (self.sequences.aides.qtest < 0.)) or                    ((self.sequences.aides.qmax > 0.) and (self.sequences.aides.qtest > 0.))):
                    self.sequences.aides.qmin = self.sequences.aides.qmin * (self.sequences.aides.qmax/(self.sequences.aides.qmax+self.sequences.aides.qtest))
                else:
                    self.sequences.aides.hmin = self.sequences.aides.hmax
                    self.sequences.aides.qmin = self.sequences.aides.qmax
                self.sequences.aides.hmax = self.sequences.fluxes.h
                self.sequences.aides.qmax = self.sequences.aides.qtest
                if fabs(self.sequences.aides.hmax-self.sequences.aides.hmin) < self.parameters.control.htol:
                    return
    cpdef inline void calc_ag_v1(self)  nogil:
        self.sequences.fluxes.ag = self.sequences.fluxes.am+self.sequences.fluxes.av[0]+self.sequences.fluxes.av[1]+self.sequences.fluxes.avr[0]+self.sequences.fluxes.avr[1]
    cpdef inline void calc_rk_v1(self)  nogil:
        if (self.sequences.fluxes.ag > 0.) and (self.sequences.fluxes.qref > 0.):
            self.sequences.fluxes.rk = (1000.*self.parameters.control.laen*self.sequences.fluxes.ag)/(self.parameters.derived.sek*self.sequences.fluxes.qref)
        else:
            self.sequences.fluxes.rk = 0.
    cpdef inline void calc_qa_v1(self)  nogil:
        if self.sequences.fluxes.rk <= 0.:
            self.sequences.new_states.qa = self.sequences.new_states.qz
        elif self.sequences.fluxes.rk > 1e200:
            self.sequences.new_states.qa = self.sequences.old_states.qa+self.sequences.new_states.qz-self.sequences.old_states.qz
        else:
            self.sequences.aides.temp = (1.-exp(-1./self.sequences.fluxes.rk))
            self.sequences.new_states.qa = (self.sequences.old_states.qa +                  (self.sequences.old_states.qz-self.sequences.old_states.qa)*self.sequences.aides.temp +                  (self.sequences.new_states.qz-self.sequences.old_states.qz)*(1.-self.sequences.fluxes.rk*self.sequences.aides.temp))
    cpdef inline void calc_qref(self)  nogil:
        self.sequences.fluxes.qref = (self.sequences.new_states.qz+self.sequences.old_states.qz+self.sequences.old_states.qa)/3.
    cpdef inline void calc_hmin_qmin_hmax_qmax(self)  nogil:
        if self.sequences.fluxes.qref <= self.parameters.derived.qm:
            self.sequences.aides.hmin = 0.
            self.sequences.aides.qmin = 0.
            self.sequences.aides.hmax = self.parameters.control.hm
            self.sequences.aides.qmax = self.parameters.derived.qm
        elif self.sequences.fluxes.qref <= min(self.parameters.derived.qv[0], self.parameters.derived.qv[1]):
            self.sequences.aides.hmin = self.parameters.control.hm
            self.sequences.aides.qmin = self.parameters.derived.qm
            self.sequences.aides.hmax = self.parameters.control.hm+min(self.parameters.derived.hv[0], self.parameters.derived.hv[1])
            self.sequences.aides.qmax = min(self.parameters.derived.qv[0], self.parameters.derived.qv[1])
        elif self.sequences.fluxes.qref < max(self.parameters.derived.qv[0], self.parameters.derived.qv[1]):
            self.sequences.aides.hmin = self.parameters.control.hm+min(self.parameters.derived.hv[0], self.parameters.derived.hv[1])
            self.sequences.aides.qmin = min(self.parameters.derived.qv[0], self.parameters.derived.qv[1])
            self.sequences.aides.hmax = self.parameters.control.hm+max(self.parameters.derived.hv[0], self.parameters.derived.hv[1])
            self.sequences.aides.qmax = max(self.parameters.derived.qv[0], self.parameters.derived.qv[1])
        else:
            self.sequences.fluxes.h = self.parameters.control.hm+max(self.parameters.derived.hv[0], self.parameters.derived.hv[1])
            self.sequences.aides.hmin = self.sequences.fluxes.h
            self.sequences.aides.qmin = self.sequences.fluxes.qg
            while True:
                self.sequences.fluxes.h = self.sequences.fluxes.h * (2.)
                self.calc_qg()
                if self.sequences.fluxes.qg < self.sequences.fluxes.qref:
                    self.sequences.aides.hmin = self.sequences.fluxes.h
                    self.sequences.aides.qmin = self.sequences.fluxes.qg
                else:
                    self.sequences.aides.hmax = self.sequences.fluxes.h
                    self.sequences.aides.qmax = self.sequences.fluxes.qg
                    break
    cpdef inline void calc_h(self)  nogil:
        self.sequences.aides.qmin = self.sequences.aides.qmin - (self.sequences.fluxes.qref)
        self.sequences.aides.qmax = self.sequences.aides.qmax - (self.sequences.fluxes.qref)
        if fabs(self.sequences.aides.qmin) < self.parameters.control.qtol:
            self.sequences.fluxes.h = self.sequences.aides.hmin
            self.calc_qg()
        elif fabs(self.sequences.aides.qmax) < self.parameters.control.qtol:
            self.sequences.fluxes.h = self.sequences.aides.hmax
            self.calc_qg()
        elif fabs(self.sequences.aides.hmax-self.sequences.aides.hmin) < self.parameters.control.htol:
            self.sequences.fluxes.h = (self.sequences.aides.hmin+self.sequences.aides.hmax)/2.
            self.calc_qg()
        else:
            while True:
                self.sequences.fluxes.h = self.sequences.aides.hmin-self.sequences.aides.qmin*(self.sequences.aides.hmax-self.sequences.aides.hmin)/(self.sequences.aides.qmax-self.sequences.aides.qmin)
                self.calc_qg()
                self.sequences.aides.qtest = self.sequences.fluxes.qg-self.sequences.fluxes.qref
                if fabs(self.sequences.aides.qtest) < self.parameters.control.qtol:
                    return
                elif (((self.sequences.aides.qmax < 0.) and (self.sequences.aides.qtest < 0.)) or                    ((self.sequences.aides.qmax > 0.) and (self.sequences.aides.qtest > 0.))):
                    self.sequences.aides.qmin = self.sequences.aides.qmin * (self.sequences.aides.qmax/(self.sequences.aides.qmax+self.sequences.aides.qtest))
                else:
                    self.sequences.aides.hmin = self.sequences.aides.hmax
                    self.sequences.aides.qmin = self.sequences.aides.qmax
                self.sequences.aides.hmax = self.sequences.fluxes.h
                self.sequences.aides.qmax = self.sequences.aides.qtest
                if fabs(self.sequences.aides.hmax-self.sequences.aides.hmin) < self.parameters.control.htol:
                    return
    cpdef inline void calc_ag(self)  nogil:
        self.sequences.fluxes.ag = self.sequences.fluxes.am+self.sequences.fluxes.av[0]+self.sequences.fluxes.av[1]+self.sequences.fluxes.avr[0]+self.sequences.fluxes.avr[1]
    cpdef inline void calc_rk(self)  nogil:
        if (self.sequences.fluxes.ag > 0.) and (self.sequences.fluxes.qref > 0.):
            self.sequences.fluxes.rk = (1000.*self.parameters.control.laen*self.sequences.fluxes.ag)/(self.parameters.derived.sek*self.sequences.fluxes.qref)
        else:
            self.sequences.fluxes.rk = 0.
    cpdef inline void calc_qa(self)  nogil:
        if self.sequences.fluxes.rk <= 0.:
            self.sequences.new_states.qa = self.sequences.new_states.qz
        elif self.sequences.fluxes.rk > 1e200:
            self.sequences.new_states.qa = self.sequences.old_states.qa+self.sequences.new_states.qz-self.sequences.old_states.qz
        else:
            self.sequences.aides.temp = (1.-exp(-1./self.sequences.fluxes.rk))
            self.sequences.new_states.qa = (self.sequences.old_states.qa +                  (self.sequences.old_states.qz-self.sequences.old_states.qa)*self.sequences.aides.temp +                  (self.sequences.new_states.qz-self.sequences.old_states.qz)*(1.-self.sequences.fluxes.rk*self.sequences.aides.temp))
    cpdef inline void calc_am_um_v1(self)  nogil:
        if self.sequences.fluxes.h <= 0.:
            self.sequences.fluxes.am = 0.
            self.sequences.fluxes.um = 0.
        elif self.sequences.fluxes.h < self.parameters.control.hm:
            self.sequences.fluxes.am = self.sequences.fluxes.h*(self.parameters.control.bm+self.sequences.fluxes.h*self.parameters.control.bnm)
            self.sequences.fluxes.um = self.parameters.control.bm+2.*self.sequences.fluxes.h*(1.+self.parameters.control.bnm**2)**.5
        else:
            self.sequences.fluxes.am = (self.parameters.control.hm*(self.parameters.control.bm+self.parameters.control.hm*self.parameters.control.bnm) +                  ((self.sequences.fluxes.h-self.parameters.control.hm)*(self.parameters.control.bm+2.*self.parameters.control.hm*self.parameters.control.bnm)))
            self.sequences.fluxes.um = (self.parameters.control.bm)+(2.*self.parameters.control.hm*(1.+self.parameters.control.bnm**2)**.5)+(2*(self.sequences.fluxes.h-self.parameters.control.hm))
    cpdef inline void calc_qm_v1(self)  nogil:
        if (self.sequences.fluxes.am > 0.) and (self.sequences.fluxes.um > 0.):
            self.sequences.fluxes.qm = self.parameters.control.ekm*self.parameters.control.skm*self.sequences.fluxes.am**(5./3.)/self.sequences.fluxes.um**(2./3.)*self.parameters.control.gef**.5
        else:
            self.sequences.fluxes.qm = 0.
    cpdef inline void calc_av_uv_v1(self)  nogil:
        cdef int i
        for i in range(2):
            if self.sequences.fluxes.h <= self.parameters.control.hm:
                self.sequences.fluxes.av[i] = 0.
                self.sequences.fluxes.uv[i] = 0.
            elif self.sequences.fluxes.h <= (self.parameters.control.hm+self.parameters.derived.hv[i]):
                self.sequences.fluxes.av[i] = (self.sequences.fluxes.h-self.parameters.control.hm)*(self.parameters.control.bv[i]+(self.sequences.fluxes.h-self.parameters.control.hm)*self.parameters.control.bnv[i]/2.)
                self.sequences.fluxes.uv[i] = self.parameters.control.bv[i]+(self.sequences.fluxes.h-self.parameters.control.hm)*(1.+self.parameters.control.bnv[i]**2)**.5
            else:
                self.sequences.fluxes.av[i] = (self.parameters.derived.hv[i]*(self.parameters.control.bv[i]+self.parameters.derived.hv[i]*self.parameters.control.bnv[i]/2.) +                         ((self.sequences.fluxes.h-(self.parameters.control.hm+self.parameters.derived.hv[i])) *                          (self.parameters.control.bv[i]+self.parameters.derived.hv[i]*self.parameters.control.bnv[i])))
                self.sequences.fluxes.uv[i] = ((self.parameters.control.bv[i])+(self.parameters.derived.hv[i]*(1.+self.parameters.control.bnv[i]**2)**.5) +                         (self.sequences.fluxes.h-(self.parameters.control.hm+self.parameters.derived.hv[i])))
    cpdef inline void calc_qv_v1(self)  nogil:
        cdef int i
        for i in range(2):
            if (self.sequences.fluxes.av[i] > 0.) and (self.sequences.fluxes.uv[i] > 0.):
                self.sequences.fluxes.qv[i] = (self.parameters.control.ekv[i]*self.parameters.control.skv[i] *                         self.sequences.fluxes.av[i]**(5./3.)/self.sequences.fluxes.uv[i]**(2./3.)*self.parameters.control.gef**.5)
            else:
                self.sequences.fluxes.qv[i] = 0.
    cpdef inline void calc_avr_uvr_v1(self)  nogil:
        cdef int i
        for i in range(2):
            if self.sequences.fluxes.h <= (self.parameters.control.hm+self.parameters.derived.hv[i]):
                self.sequences.fluxes.avr[i] = 0.
                self.sequences.fluxes.uvr[i] = 0.
            else:
                self.sequences.fluxes.avr[i] = (self.sequences.fluxes.h-(self.parameters.control.hm+self.parameters.derived.hv[i]))**2*self.parameters.control.bnvr[i]/2.
                self.sequences.fluxes.uvr[i] = (self.sequences.fluxes.h-(self.parameters.control.hm+self.parameters.derived.hv[i]))*(1.+self.parameters.control.bnvr[i]**2)**.5
    cpdef inline void calc_qvr_v1(self)  nogil:
        cdef int i
        for i in range(2):
            if (self.sequences.fluxes.avr[i] > 0.) and (self.sequences.fluxes.uvr[i] > 0.):
                self.sequences.fluxes.qvr[i] = (self.parameters.control.ekv[i]*self.parameters.control.skv[i] *                          self.sequences.fluxes.avr[i]**(5./3.)/self.sequences.fluxes.uvr[i]**(2./3.)*self.parameters.control.gef**.5)
            else:
                self.sequences.fluxes.qvr[i] = 0.
    cpdef inline void calc_qg_v1(self)  nogil:
        self.calc_am_um()
        self.calc_qm()
        self.calc_av_uv()
        self.calc_qv()
        self.calc_avr_uvr()
        self.calc_qvr()
        self.sequences.fluxes.qg = self.sequences.fluxes.qm+self.sequences.fluxes.qv[0]+self.sequences.fluxes.qv[1]+self.sequences.fluxes.qvr[0]+self.sequences.fluxes.qvr[1]
    cpdef inline void calc_am_um(self)  nogil:
        if self.sequences.fluxes.h <= 0.:
            self.sequences.fluxes.am = 0.
            self.sequences.fluxes.um = 0.
        elif self.sequences.fluxes.h < self.parameters.control.hm:
            self.sequences.fluxes.am = self.sequences.fluxes.h*(self.parameters.control.bm+self.sequences.fluxes.h*self.parameters.control.bnm)
            self.sequences.fluxes.um = self.parameters.control.bm+2.*self.sequences.fluxes.h*(1.+self.parameters.control.bnm**2)**.5
        else:
            self.sequences.fluxes.am = (self.parameters.control.hm*(self.parameters.control.bm+self.parameters.control.hm*self.parameters.control.bnm) +                  ((self.sequences.fluxes.h-self.parameters.control.hm)*(self.parameters.control.bm+2.*self.parameters.control.hm*self.parameters.control.bnm)))
            self.sequences.fluxes.um = (self.parameters.control.bm)+(2.*self.parameters.control.hm*(1.+self.parameters.control.bnm**2)**.5)+(2*(self.sequences.fluxes.h-self.parameters.control.hm))
    cpdef inline void calc_qm(self)  nogil:
        if (self.sequences.fluxes.am > 0.) and (self.sequences.fluxes.um > 0.):
            self.sequences.fluxes.qm = self.parameters.control.ekm*self.parameters.control.skm*self.sequences.fluxes.am**(5./3.)/self.sequences.fluxes.um**(2./3.)*self.parameters.control.gef**.5
        else:
            self.sequences.fluxes.qm = 0.
    cpdef inline void calc_av_uv(self)  nogil:
        cdef int i
        for i in range(2):
            if self.sequences.fluxes.h <= self.parameters.control.hm:
                self.sequences.fluxes.av[i] = 0.
                self.sequences.fluxes.uv[i] = 0.
            elif self.sequences.fluxes.h <= (self.parameters.control.hm+self.parameters.derived.hv[i]):
                self.sequences.fluxes.av[i] = (self.sequences.fluxes.h-self.parameters.control.hm)*(self.parameters.control.bv[i]+(self.sequences.fluxes.h-self.parameters.control.hm)*self.parameters.control.bnv[i]/2.)
                self.sequences.fluxes.uv[i] = self.parameters.control.bv[i]+(self.sequences.fluxes.h-self.parameters.control.hm)*(1.+self.parameters.control.bnv[i]**2)**.5
            else:
                self.sequences.fluxes.av[i] = (self.parameters.derived.hv[i]*(self.parameters.control.bv[i]+self.parameters.derived.hv[i]*self.parameters.control.bnv[i]/2.) +                         ((self.sequences.fluxes.h-(self.parameters.control.hm+self.parameters.derived.hv[i])) *                          (self.parameters.control.bv[i]+self.parameters.derived.hv[i]*self.parameters.control.bnv[i])))
                self.sequences.fluxes.uv[i] = ((self.parameters.control.bv[i])+(self.parameters.derived.hv[i]*(1.+self.parameters.control.bnv[i]**2)**.5) +                         (self.sequences.fluxes.h-(self.parameters.control.hm+self.parameters.derived.hv[i])))
    cpdef inline void calc_qv(self)  nogil:
        cdef int i
        for i in range(2):
            if (self.sequences.fluxes.av[i] > 0.) and (self.sequences.fluxes.uv[i] > 0.):
                self.sequences.fluxes.qv[i] = (self.parameters.control.ekv[i]*self.parameters.control.skv[i] *                         self.sequences.fluxes.av[i]**(5./3.)/self.sequences.fluxes.uv[i]**(2./3.)*self.parameters.control.gef**.5)
            else:
                self.sequences.fluxes.qv[i] = 0.
    cpdef inline void calc_avr_uvr(self)  nogil:
        cdef int i
        for i in range(2):
            if self.sequences.fluxes.h <= (self.parameters.control.hm+self.parameters.derived.hv[i]):
                self.sequences.fluxes.avr[i] = 0.
                self.sequences.fluxes.uvr[i] = 0.
            else:
                self.sequences.fluxes.avr[i] = (self.sequences.fluxes.h-(self.parameters.control.hm+self.parameters.derived.hv[i]))**2*self.parameters.control.bnvr[i]/2.
                self.sequences.fluxes.uvr[i] = (self.sequences.fluxes.h-(self.parameters.control.hm+self.parameters.derived.hv[i]))*(1.+self.parameters.control.bnvr[i]**2)**.5
    cpdef inline void calc_qvr(self)  nogil:
        cdef int i
        for i in range(2):
            if (self.sequences.fluxes.avr[i] > 0.) and (self.sequences.fluxes.uvr[i] > 0.):
                self.sequences.fluxes.qvr[i] = (self.parameters.control.ekv[i]*self.parameters.control.skv[i] *                          self.sequences.fluxes.avr[i]**(5./3.)/self.sequences.fluxes.uvr[i]**(2./3.)*self.parameters.control.gef**.5)
            else:
                self.sequences.fluxes.qvr[i] = 0.
    cpdef inline void calc_qg(self)  nogil:
        self.calc_am_um()
        self.calc_qm()
        self.calc_av_uv()
        self.calc_qv()
        self.calc_avr_uvr()
        self.calc_qvr()
        self.sequences.fluxes.qg = self.sequences.fluxes.qm+self.sequences.fluxes.qv[0]+self.sequences.fluxes.qv[1]+self.sequences.fluxes.qvr[0]+self.sequences.fluxes.qvr[1]
    cpdef inline void pick_q_v1(self)  nogil:
        cdef int idx
        self.sequences.states.qz = 0.
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.states.qz = self.sequences.states.qz + (self.sequences.inlets.q[idx][0])
    cpdef inline void pick_q(self)  nogil:
        cdef int idx
        self.sequences.states.qz = 0.
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.states.qz = self.sequences.states.qz + (self.sequences.inlets.q[idx][0])
    cpdef inline void pass_q_v1(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.states.qa)
    cpdef inline void pass_q(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.states.qa)
