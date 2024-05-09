# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 19:20:57 2022

@author: jced0001
"""
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!WARNING: RUNNING run_test() WILL CHANGE SETTINGS IN NANONIS. RUN IT ON A SIM!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

from nanonisTCP import nanonisTCP
from nanonisTCP.LockIn import LockIn
import traceback

def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501, debug=False, version=13520):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT, version=version)                        # Nanonis TCP interface
    try:
        lockin = LockIn(NTCP)                                                   # Nanonis TCP Lock In Module
        
        """
        On/Off Set/Get
        """
        lockin.ModOnOffSet(modulator_number=1,lockin_onoff=1)
        lockin1 = lockin.ModOnOffGet(modulator_number=1)
        lockin2 = lockin.ModOnOffGet(modulator_number=2)
        if(debug):
            print("lockin1: " + ["off","on"][lockin1])
            print("lockin2: " + ["off","on"][lockin2])
            print("----------------------------------------------------------------------")
        
        """
        ModSignalSet/Get
        """
        lockin.ModSignalSet(modulator_number=1,modulator_signal_index=24)       # Make sure the signal index you give is available with Signals.NamesGet
        modulator_signal_index1  = lockin.ModSignalGet(modulator_number=1)
        modulator_signal_index2  = lockin.ModSignalGet(modulator_number=2)
        if(debug):
            print("Signal1: " + str(modulator_signal_index1))
            print("Signal2: " + str(modulator_signal_index2))
            print("----------------------------------------------------------------------")
        
        """
        ModPhasRegSet/Get
        """
        try:
            lockin.ModPhasRegSet(modulator_number=1,phase_register_index=2)     # Access denied error in demo mode
        except Exception as e:
            print("Warning: Could not set phase register. " + str(e))
        phase_reg1 = lockin.ModPhasRegGet(modulator_number=1)
        phase_reg2 = lockin.ModPhasRegGet(modulator_number=2)
        if(debug):
            print("Signal1: " + str(phase_reg1))
            print("Signal2: " + str(phase_reg2))
            print("----------------------------------------------------------------------")
        
        """
        ModHarmonicSet/Get
        """
        try:
            lockin.ModHarmonicSet(modulator_number=1,harmonic=2)                # Access denied error in demo mode
        except Exception as e:
            print("Warning: Could not set phase register. " + str(e))
        harmonic1 = lockin.ModHarmonicGet(modulator_number=1)
        harmonic2 = lockin.ModHarmonicGet(modulator_number=2)
        if(debug):
            print("Harmonic1: " + str(harmonic1))
            print("Harmonic2: " + str(harmonic2))
            print("----------------------------------------------------------------------")
        
        """
        ModPhasSet/Get
        """
        try:
            lockin.ModPhasSet(modulator_number=1,phase_deg=99)                  # Access denied error in demo mode
        except Exception as e:
            print("Warning: Could not set phase. " + str(e))
        phase1 = lockin.ModPhasGet(modulator_number=1)
        phase2 = lockin.ModPhasGet(modulator_number=2)
        if(debug):
            print("Phase1: " + str(phase1))
            print("Phase2: " + str(phase2))
            print("----------------------------------------------------------------------")
        
        """
        ModAmpSet/Get
        """
        try:
            lockin.ModAmpSet(modulator_number=1,amplitude=2)                    # Access denied error in demo mode
        except Exception as e:
            print("Warning: Could not set amplitude. " + str(e))
        amplitude1 = lockin.ModAmpGet(modulator_number=1)
        amplitude2 = lockin.ModAmpGet(modulator_number=2)
        if(debug):
            print("Amplitude1: " + str(amplitude1))
            print("Amplitude2: " + str(amplitude2))
            print("----------------------------------------------------------------------")
        
        """
        ModPhasFreqSet/Get
        """
        try:
            lockin.ModPhasFreqSet(modulator_number=1,frequency=2e3)             # Access denied error in demo mode
        except Exception as e:
            print("Warning: Could not set frequency. " + str(e))
        frequency1 = lockin.ModPhasFreqGet(modulator_number=1)
        frequency2 = lockin.ModPhasFreqGet(modulator_number=2)
        if(debug):
            print("Frequency1: " + str(frequency1))
            print("frequency2: " + str(frequency2))
            print("----------------------------------------------------------------------")
        
        """
        DemodSignalSet/Get
        """
        lockin.DemodSignalSet(demod_number=1,demod_signal_index=1)
        demod_signal_index1 = lockin.DemodSignalGet(demod_number=1)
        demod_signal_index2 = lockin.DemodSignalGet(demod_number=2)
        if(debug):
            print("Signal1: " + str(demod_signal_index1))
            print("Signal2: " + str(demod_signal_index2))
            print("----------------------------------------------------------------------")
        
        """
        DemodLPFilterSet/Get
        """
        try:
            lockin.DemodLPFilterSet(demod_number=1,lp_filter_order=1,cutoff=2e3)# Access denied error in demo mode
        except Exception as e:
            print("Warning: Could not set lpfilter. " + str(e))
        lpfilter1 = lockin.DemodLPFilterGet(demod_number=1)
        lpfilter2 = lockin.DemodLPFilterGet(demod_number=2)
        if(debug):
            print("LP Filter1: " + str(lpfilter1))
            print("LP Filter2: " + str(lpfilter2))
            print("----------------------------------------------------------------------")
        
        """
        DemodPhasRegSet/Get
        """
        try:
            lockin.DemodPhasRegSet(demod_number=1,phase_register_index=1)       # Access denied error in demo mode
        except Exception as e:
            print("Warning: Could not set phase register. " + str(e))
        phase_reg1 = lockin.DemodPhasRegGet(demod_number=1)
        phase_reg2 = lockin.DemodPhasRegGet(demod_number=2)
        if(debug):
            print("Phase Register1: " + str(phase_reg1))
            print("Phase Register2: " + str(phase_reg2))
            print("----------------------------------------------------------------------")
        
        """
        DemodPhasSet/Get
        """
        try:
            lockin.DemodPhasSet(demod_number=1,phase_deg=98)                    # Access denied error in demo mode
        except Exception as e:
            print("Warning: Could not set phase. " + str(e))
        phase1 = lockin.DemodPhasGet(demod_number=1)
        phase2 = lockin.DemodPhasGet(demod_number=2)
        if(debug):
            print("Phase1: " + str(phase1))
            print("Phase2: " + str(phase2))
            print("----------------------------------------------------------------------")
        
        """
        DemodSyncFilterSet/Get
        """
        try:
            lockin.DemodSyncFilterSet(demod_number=1,sync_filter=0)             # Access denied error in demo mode
        except Exception as e:
            print("Warning: Could not set sync filter. " + str(e))
        syncFilter1 = lockin.DemodSyncFilterGet(demod_number=1)
        syncFilter2 = lockin.DemodSyncFilterGet(demod_number=2)
        if(debug):
            print("syncFilter1: " + str(syncFilter1))
            print("syncFilter2: " + str(syncFilter2))
            print("----------------------------------------------------------------------")
        
        """
        DemodRTSignalsSet/Get
        """
        try:
            lockin.DemodRTSignalsSet(demod_number=1,rt_signals=1)               # Access denied error in demo mode
        except Exception as e:
            print("Warning: Could not set RT Signals. " + str(e))
        rtSignals1 = lockin.DemodRTSignalsGet(demod_number=1)
        rtSignals2 = lockin.DemodRTSignalsGet(demod_number=2)
        if(debug):
            print("rtSignals1: " + str(rtSignals1))
            print("rtSignals2: " + str(rtSignals2))
            print("----------------------------------------------------------------------")
    except:
        NTCP.close_connection()
        return traceback.format_exc()
        
    NTCP.close_connection()
    return "success"
        