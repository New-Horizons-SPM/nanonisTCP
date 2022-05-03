# -*- coding: utf-8 -*-
"""
Created on Tue May  3 19:09:44 2022

@author: Julian
"""

from nanonisTCP import nanonisTCP
from nanonisTCP.AutoApproach import AutoApproach

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6502, make_plot=False):
    
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT)                                         # Nanonis TCP interface
    
    autoApp = AutoApproach(NTCP)                                                # Nanonis Auto Approach Module
    
    try:
        """
        Open
        """
        autoApp.Open()
        
        """
        On/Off Set/Get
        """
        autoApp.OnOffSet(on_off=True)
        on_off = autoApp.OnOffGet()
        print("Auto Approach On/Off")
        print("Status: " + ["Off","Running"][on_off])
        print("----------------------------------------------------------------------")
    except Exception as e:
        print(e)
    
    NTCP.close_connection()