
if __name__ == '__main__':
    import sys
    sys.path.insert(0, r'C:\HydPy\HydPy')

    from hydpy import *

    hp = HydPy('LahnHBV')
    pub.timegrids = '1996-01-01', '2007-01-01', '1d'
    pub.sequencemanager.inputfiletype = 'npy'
    hp.prepare_network()
    hp.init_models()
    hp.prepare_inputseries()
    hp.load_inputseries()

    pub.sequencemanager.inputfiletype = 'nc'
    pub.sequencemanager.open_netcdf_writer(flatten=True, isolate=True)
    hp.save_inputseries()
    pub.sequencemanager.close_netcdf_writer()
