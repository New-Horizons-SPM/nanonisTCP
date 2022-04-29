#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 16:56:08 2022

@author: jack
"""

from NanonisTCP import NanonisTCP
from Bias       import Bias

"""
Set up the TCP connection and interface
"""
TCP_IP = '127.0.0.1'
TCP_PORT = 6501                                                                 # Listening Port: see Nanonis File>Settings>TCP Programming Interface
NTCP = NanonisTCP(TCP_IP, TCP_PORT)                                             # Nanonis TCP interface

"""
Bias Set/Get
"""
bias = Bias(NTCP)                                                               # Nanonis Bias Module

bias.Set(5)                                                                     # Set bias to 5 V
v = bias.Get()                                                                  # Get the current bias
print("Bias Get")
print("Bias: " + str(v) + " V")
print("----------------------------------------------------------------------")

"""
Range Set/Get
"""
bias.RangeSet(0)
bias_ranges, bias_range_index = bias.RangeGet()

"""
Calibration Set/Get
"""
bias.CalibrSet(calibration=2, offset=-0.1)
calibration,offset = bias.CalibrGet()
print("Calibration")
print("Calibration: " + str(calibration))
print("Offset:      " + str(offset))
print("----------------------------------------------------------------------")

"""
Pulse
"""
bias.Pulse(0.25, -3,z_hold=1,rel_abs=1,wait_until_done=True)
NTCP.close_connection()
