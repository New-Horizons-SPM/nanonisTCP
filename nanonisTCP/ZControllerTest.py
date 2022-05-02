# -*- coding: utf-8 -*-
"""
Created on Mon May  2 15:36:03 2022

@author: jced0001
"""

import time
from nanonisTCP import nanonisTCP
from nanonisTCP.ZController import ZController

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6502, make_plot=False):
    
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT)                                         # Nanonis TCP interface
    
    zctrl = ZController(NTCP)                                                   # Nanonis Z-Controller Module
    
    try:
        """
        ZPos Set/Get
        """
        zctrl.ZPosSet(140e-9)
        zpos = zctrl.ZPosGet()
        print("Z-Controller ZPos")
        print("zpos: " + str(zpos) + " m")
        print("----------------------------------------------------------------------")
        
        """
        OnOff Set/Get
        """
        zctrl.OnOffSet(on=False)
        time.sleep(1)                                                           # Need to sleep otherwise it doesn't update in time
        z_status = zctrl.OnOffGet()
        print("Z-Controller Status")
        print("Controller: " + ["Off","On"][z_status])
        print("----------------------------------------------------------------------")
        
        """
        Setpnt Set/Get
        """
        zctrl.SetpntSet(27e-12)
        setpoint = zctrl.SetpntGet()
        print("Z-Controller Setpoint")
        print("Setpoint: " + str(setpoint) + " A")
        print("----------------------------------------------------------------------")
        
        """
        Gain Set/Get
        """
        zctrl.GainSet(3e-12, 155e-6)
        p_gain,time_constant,i_gain = zctrl.GainGet()
        print("Z-Controller Gain")
        print("proportional gain: " + str(p_gain))
        print("integral gain:     " + str(i_gain))
        print("time constant:     " + str(time_constant))
        print("----------------------------------------------------------------------")
        
    except:
        print("error")
    
    NTCP.close_connection()