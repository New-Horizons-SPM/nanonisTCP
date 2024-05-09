# -*- coding: utf-8 -*-
"""
Created on Mon May 30 12:41:36 2022

@author: Julian Ceddia
"""
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!WARNING: RUNNING run_test() WILL CHANGE SETTINGS IN NANONIS. RUN IT ON A SIM!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

from nanonisTCP import nanonisTCP
from nanonisTCP.Signals import Signals
import traceback

def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501, version=13520, debug=False):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT, version=version)                        # Nanonis TCP interface
    try:
        signalsModule = Signals(NTCP)                                           # Nanonis TCP Signals Module
        
        """
        Signals NamesGet
        """
        signal_names = signalsModule.NamesGet()
        if(debug):
            print("Signals NamesGet")
            print("Signal names:\n" + "\n".join(signal_names))
            print("----------------------------------------------------------------------")
        
        """
        Signals InSlots Set/Get
        """
        if(version < 11798):                                                    # Deprecated in version 11798
            signalsModule.InSlotSet(slot=5, RTSignalIndex=10)                   # Puts "Input 11 (V)" into slot index 5 of 24
            signal_names,signal_indexes = signalsModule.InSlotsGet()
            if(debug):
                print("Signals InSlots")
                for i,signal_name in enumerate(signal_names):
                    print("signal " + str(i) + ": " + str(signal_indexes[i]) + "| " + signal_name)
                print("----------------------------------------------------------------------")
        
        """
        Signals CalibrGet
        """
        calibration,offset = signalsModule.CalibrGet(24)
        if(debug):
            print("Signals CalibrGet")
            print("Calibration: " + str(calibration))
            print("Offset:      " + str(offset))
            print("----------------------------------------------------------------------")
        
        """
        Signals RangeGet
        """
        max_limit,min_limit = signalsModule.RangeGet(24)
        if(debug):
            print("Signals RageGet")
            print("Max limit: " + str(max_limit))
            print("Min limit: " + str(min_limit))
            print("----------------------------------------------------------------------")
        
        """
        Signals GetVal
        """
        signal_val = signalsModule.ValGet(2)
        if(debug):
            print("Signals GetVal")
            print("Signal value: " + str(signal_val))
            print("----------------------------------------------------------------------")
    except:
        NTCP.close_connection()
        return(traceback.format_exc())
    
    NTCP.close_connection()
    return "success"