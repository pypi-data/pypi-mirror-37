#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 15:02:57 2018

@author: aguimera
"""

import neo
import numpy as np
import quantities as pq
import matplotlib.pylab as plt


class NeoSegment(neo.Segment):
    pass


class NeoSignal(neo.AnalogSignal):
    def CheckTime(self, Time):
        if Time is None:
            return (self.t_start, self.t_stop)

        if len(Time) == 1:
            Time = (Time[0], Time[0] + self.sampling_period)

        if Time[0] is None or Time[0] < self.t_start:
            Tstart = self.t_start
        else:
            Tstart = Time[0]

        if Time[1] is None or Time[1] > self.t_stop:
            Tstop = self.t_stop
        else:
            Tstop = Time[1]

        return (Tstart, Tstop)

    def GetSignal(self, Time, Units=None):
        time = self.CheckTime(Time)

        sl = self.time_slice(time[0], time[1])

        if Units is None:
            return sl
        else:
            return sl.rescale(Units)


if __name__ == '__main__':
    t = np.arange(0, 1, 1.0/1000)
    test = NeoSignal(1*np.sin(2*np.pi*10*t),
                     name='t',
                     sampling_rate=1000*pq.Hz,
                     units='V')
    
    plt.plot(test.times, test)
    
    sig = test.GetSignal((0.5*pq.s, 0.8*pq.s))
    plt.plot(sig.times, sig)
    
    t = np.arange(0, 1, 1.0/500)
    AnalogSig = neo.AnalogSignal(2*np.sin(2*np.pi*10*t),
                            name='t',
                            sampling_rate=500*pq.Hz,
                            units='V')
    
    AnalogSig.__class__ = NeoSignal
    
    sig = AnalogSig.GetSignal((0.5*pq.s, 0.8*pq.s))
    plt.plot(sig.times, sig)

    

#    Rec = NeoSegment()
    
    