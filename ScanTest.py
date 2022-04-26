# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 12:24:35 2022

@author: jced0001
"""

from NanonisTCP import NanonisTCP
from Scan       import Scan

"""
Set up the TCP connection and interface
"""
TCP_IP = '127.0.0.1'
TCP_PORT = 6501                                                                 # Listening Port: see Nanonis File>Settings>TCP Programming Interface
NTCP = NanonisTCP(TCP_IP, TCP_PORT)                                             # Nanonis TCP interface

scan = Scan(NTCP)                                                               # Nanonis Scan Module

"""
Action
"""
scan.Action("start","down")

"""
Status Get
"""

"""
Wait end of scan
"""
timeout_status, file_path_size, file_path = scan.WaitEndOfScan()
print("timeout_status: " + ["EOS","Timed out"][timeout_status])
print("file_path: " + file_path)

"""
Frame Parameters Set/Get
"""
scan.FrameSet(5e-9,-5e-9,30e-9,30e-9,15)
x,y,w,h,angle = scan.FrameGet()
print("Frame Position:  " + str(x) + " m," + str(y) + " m")
print("Frame dimension: " + str(w) + " m x " + str(h) + " m")
print("Frame angle:     " + str(angle) + " deg")

"""
Buffer Parameters Set/Get
"""
scan.BufferSet([0,1], 512, 512)

NTCP.close_connection()
