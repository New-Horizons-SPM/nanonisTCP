#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 16:56:08 2022

@author: jack
"""

from NanonisTCP import NanonisTCP
from Bias       import Bias
from FolMe      import FolMe

"""
Set up the TCP connection and interface
"""
TCP_IP = '127.0.0.1'
TCP_PORT = 6501                                                                 # Listening Port: see Nanonis File>Settings>TCP Programming Interface
NTCP = NanonisTCP(TCP_IP, TCP_PORT)                                             # Nanonis TCP interface

"""
Bias Module: Set/Get Bias example
"""
bias = Bias(NTCP)                                                               # Nanonis Bias Module

bias.Set(5)                                                                     # Set bias to 7 V
v = bias.Get()                                                                  # Get the current bias
print("Bias: " + str(v) + " V")

"""
Follow Me Module: Set/Get XY Pos example
"""
followme = FolMe(NTCP)                                                          # Nanonis Follow Me Module

followme.XYPosSet(5e-9, -5e-9, Wait_end_of_move=True)                           # Set xy pos to 5 nm, -5 nm
x,y = followme.XYPosGet(Wait_for_newest_data=True)                              # Get the current XY tip position
print("Tip Position: " + str(x) + " nm, " + str(y) + " nm")    

NTCP.close_connection()