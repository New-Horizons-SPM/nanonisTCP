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
print("Bias: " + str(v) + " V")

NTCP.close_connection()
