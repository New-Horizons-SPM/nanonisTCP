# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:17:56 2022

@author: Julian Ceddia
"""
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!WARNING: RUNNING run_test() WILL CHANGE SETTINGS IN NANONIS. RUN IT ON A SIM!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

from nanonisTCP import nanonisTCP
from nanonisTCP.SafeTip import SafeTip
import traceback

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6502, make_plot=False, debug=False, version=13520):
    
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT, version=version)                        # Nanonis TCP interface
    
    safeTip = SafeTip(NTCP)                                                     # Nanonis Safe Tip Module
    
    try:
        """
        On/Off Set/Get
        """
        safeTip.OnOffSet(safe_tip_status=2)
        safe_tip_status = safeTip.OnOffGet()
        if(debug):
            print("Safe Tip Status")
            print("Safe Tip Mode:  " + ["off","on"][safe_tip_status])
            print("----------------------------------------------------------------------")
        
        """
        Signal Get
        """
        signal_value = safeTip.SignalGet()
        if(debug):
            print("Safe Tip Signal")
            print("Signal value:  " + str(signal_value) + " A")
            print("----------------------------------------------------------------------")
        
        """
        Properties Set/Get
        """
        safeTip.PropsSet(auto_recovery=True,auto_pause_scan=True,threshold=15e-10)
        auto_recovery,auto_pause_scan,threshold = safeTip.PropsGet()
        if(debug):
            print("Safe Tip Properties")
            print("Auto recovery:  " + ["Off","On"][auto_recovery])
            print("Auto pause:     " + ["Off","On"][auto_pause_scan])
            print("Threshold:      " + str(threshold) + " A")
            print("----------------------------------------------------------------------")
    except:
        NTCP.close_connection()
        return traceback.format_exc()
        
    NTCP.close_connection()
    return "success"