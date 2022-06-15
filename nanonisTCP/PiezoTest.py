# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 23:09:19 2022

@author: jced0001
"""
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!WARNING: RUNNING run_test() WILL CHANGE SETTINGS IN NANONIS. RUN IT ON A SIM!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

from nanonisTCP import nanonisTCP
# from Piezo import Piezo
from nanonisTCP.Piezo import Piezo

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT)                                         # Nanonis TCP interface
    try:
        piezo = Piezo(NTCP)                                                     # Nanonis TCP Piezo Module
        
        """
        Tilt Set/Get
        """
        piezo.TiltSet(0.1,-0.2)
        tilt_x,tilt_y = piezo.TiltGet()
        print("Piezo Tilt")
        print("Tilt x: " + str(tilt_x))
        print("Tilt y: " + str(tilt_y))
        print("----------------------------------------------------------------------")
        
        """
        Range Set/Get
        """
        piezo.RangeSet(1e-6,1e-6,360e-9)
        range_x,range_y,range_z = piezo.RangeGet()
        print("Piezo Ranges")
        print("Range x: " + str(range_x) + " m")
        print("Range y: " + str(range_y) + " m")
        print("Range z: " + str(range_z) + " m")
        print("----------------------------------------------------------------------")
        
        
        """
        Compensation Set/Get
        """
        piezo.DriftCompSet(on=True,vx=1e-15,vy=2e-15,vz=3e-15)
        status,vx,vy,vz,xstat,ystat,zstat = piezo.DriftCompGet()
        print("Piezo drift compensation")
        print("Status: " + str(status))
        print("X: " + str(vx) + " m/s")
        print("Y: " + str(vy) + " m/s")
        print("Z: " + str(vz) + " m/s")
        print("----------------------------------------------------------------------")
        
    except Exception as e:
        print(str(e))
    NTCP.close_connection()
    return print('end of test')

