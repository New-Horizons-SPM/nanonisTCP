# -*- coding: utf-8 -*-
"""
Created on Tue Feb 2 18:56:49 2024

@author: jced0001
"""

from nanonisTCP import nanonisTCP
from UserOut import UserOut

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT)                                             # Nanonis TCP interface
    try:
        userOut = UserOut(NTCP)                                                         # Nanonis User Outs Module

        """
        Output Mode Set/Get
        """
        userOut.ModeSet(2,1)                                                            # Set Out2 to Monitor
        output_mode = userOut.ModeGet(2)                                                # Check to see if the mode for Output2 has changed
        print("UserOut ModeGet")
        print("Output Mode: ",["User Output","Monitor","Calc.Signal"][output_mode])
        print("----------------------------------------------------------------------")

        """
        Output Monitor Set/Get
        """
        userOut.MonitorChSet(2,1)                                                       # Set the monitor channel to index 1 for output 2
        monitor_index = userOut.MonitorChGet(2)                                         # Check to see if it changed.
        print("UserOut MonitorChGet")
        print("Monitor index: ",monitor_index)
        print("----------------------------------------------------------------------")

        """
        Output Val Set
        (There is no Get in the protocol)
        """
        userOut.ValSet(8,3.3)
        
        """
        Output Calibration Set
        (There is no Get in the protocol)
        """
        userOut.CalibrSet(8,0.2,0.1)

        """
        Output CalcSignalName Set/Get
        """
        userOut.CalcSignalNameSet(8,"Output 8 Test")
        calculated_signal_name = userOut.CalcSignalNameGet(8)
        print("UserOut CalcSignalNameGet")
        print("Signal name: ",calculated_signal_name)
        print("----------------------------------------------------------------------")

        """
        Output CalcSignalConfig Set/Get
        """
        userOut.CalcSignalConfigSet(8,1,2,1)
        signal_1,operation,signal_2 = userOut.CalcSignalConfigGet(8)
        print("UserOut CalcSignalConfiGet")
        print("Signal 1:  ",signal_1)
        print("Operation: ",operation)
        print("Signal 2:  ",signal_2)
        print("----------------------------------------------------------------------")

        """
        Output Limits Get/Set
        """
        userOut.LimitsSet(8,-3.3,4.3)
        lower_limit,upper_limit = userOut.LimitsGet(8)
        print("UserOut Limits Get")
        print("Lower Limit:",lower_limit)
        print("Upper Limit:",upper_limit)
        print("----------------------------------------------------------------------")
    except Exception as e:
        print('error',e)
    NTCP.close_connection()
    return print('end of test')

run_test()