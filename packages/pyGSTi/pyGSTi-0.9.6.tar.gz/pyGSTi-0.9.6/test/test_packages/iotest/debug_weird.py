import unittest
import os,sys
import numpy as np
import pickle
import collections

import pygsti
from pygsti.construction import std1Q_XY as std
import pygsti.io.json as json
import pygsti.io.msgpack as msgpack


def main():
    std.gs_target._check_paramvec()
    gateset = std.gs_target
    
    germs = pygsti.construction.gatestring_list( [('Gx',), ('Gy',) ] ) #abridged for speed
    fiducials = std.fiducials
    maxLens = [1,2]
    gateLabels = list(gateset.gates.keys())
    
    lsgstStrings = pygsti.construction.make_lsgst_lists(
        gateLabels, fiducials, fiducials, germs, maxLens )
    
    datagen_gateset = gateset.depolarize(gate_noise=0.05, spam_noise=0.1)
    test = datagen_gateset.copy()
    ds = pygsti.construction.generate_fake_data(
        datagen_gateset, lsgstStrings[-1],
        nSamples=1000,sampleError='binomial', seed=100)
    
    #Make an gateset with instruments
    E = datagen_gateset.povms['Mdefault']['0']
    Erem = datagen_gateset.povms['Mdefault']['1']
    Gmz_plus = np.dot(E,E.T)
    Gmz_minus = np.dot(Erem,Erem.T)
    gs_withInst = datagen_gateset.copy()
    gs_withInst.instruments['Iz'] = pygsti.obj.Instrument({'plus': Gmz_plus, 'minus': Gmz_minus})
    gs_withInst.instruments['Iztp'] = pygsti.obj.TPInstrument({'plus': Gmz_plus, 'minus': Gmz_minus})
    
    results = pygsti.do_long_sequence_gst(
        ds, std.gs_target, fiducials, fiducials,
        germs, maxLens)

main()
