#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 16:56:08 2022

@author: Julian Ceddia
"""
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!WARNING: RUNNING run_test() WILL CHANGE SETTINGS IN NANONIS. RUN IT ON A SIM!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""


from nanonisTCP import nanonisTCP
from nanonisTCP.Bias import Bias
import traceback

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501, debug=True, version=13520):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT, version=version)                                # Nanonis TCP interface
    try:

        """
        Bias Set/Get
        """
        bias = Bias(NTCP)                                                               # Nanonis Bias Module

        bias.Set(5)                                                                     # Set bias to 5 V
        v = bias.Get()                                                                  # Get the current bias
        if(debug):
            print("Bias Get")
            print("Bias: " + str(v) + " V")
            print("----------------------------------------------------------------------")

        """
        Range Set/Get
        """
        bias.RangeSet(0)
        bias_ranges, bias_range_index = bias.RangeGet()
        if(debug):
            print("Bias Range")
            print("Ranges:      " + str(bias_ranges))
            print("Range index: " + str(bias_range_index))
            print("----------------------------------------------------------------------")

        """
        Calibration Set/Get
        """
        bias.CalibrSet(calibration=2, offset=-0.1)
        calibration,offset = bias.CalibrGet()
        if(debug):
            print("Calibration")
            print("Calibration: " + str(calibration))
            print("Offset:      " + str(offset))
            print("----------------------------------------------------------------------")

        """
        Pulse
        """
        bias.Pulse(0.25, -3,z_hold=1,rel_abs=1,wait_until_done=True)
    except:
        NTCP.close_connection()
        return(traceback.format_exc())
    
    NTCP.close_connection()
    return "success"