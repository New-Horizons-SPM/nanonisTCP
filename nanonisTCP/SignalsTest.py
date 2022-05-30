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

def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT)                                         # Nanonis TCP interface
    try:
        signalsModule = Signals(NTCP)                                           # Nanonis TCP Signals Module
        
        """
        Signals NamesGet
        """
        signal_names = signalsModule.NamesGet()
        print("Signals NamesGet")
        print("Signal names:\n" + "\n".join(signal_names))
        print("----------------------------------------------------------------------")
        
        """
        Signals InSlots Set/Get
        """
        signalsModule.InSlotSet(slot=5, RTSignalIndex=10)                       # Puts "Input 11 (V)" into slot index 5 of 24
        signal_names,signal_indexes = signalsModule.InSlotsGet()
        print("Signals InSlots")
        for i,signal_name in enumerate(signal_names):
            print("signal " + str(i) + ": " + str(signal_indexes[i]) + "| " + signal_name)
        print("----------------------------------------------------------------------")
        
        """
        Signals CalibrGet
        """
        calibration,offset = signalsModule.CalibrGet(24)
        print("Signals CalibrGet")
        print("Calibration: " + str(calibration))
        print("Offset:      " + str(offset))
        print("----------------------------------------------------------------------")
        
        """
        Signals RangeGet
        """
        max_limit,min_limit = signalsModule.RangeGet(24)
        print("Signals RageGet")
        print("Max limit: " + str(max_limit))
        print("Min limit: " + str(min_limit))
        print("----------------------------------------------------------------------")
        
        """
        Signals GetVal
        """
        signal_val = signalsModule.ValGet(2)
        print("Signals GetVal")
        print("Signal value: " + str(signal_val))
        print("----------------------------------------------------------------------")
    except Exception as e:
        print(str(e))
    NTCP.close_connection()
    return print('end of test')