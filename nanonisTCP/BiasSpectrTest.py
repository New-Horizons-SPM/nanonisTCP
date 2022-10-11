# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 23:12:28 2022

@author: Julian
"""
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!WARNING: RUNNING run_test() WILL CHANGE SETTINGS IN NANONIS. RUN IT ON A SIM!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

from nanonisTCP import nanonisTCP
# from nanonisTCP.BiasSpectr import BiasSpectr
from BiasSpectr import BiasSpectr
import traceback
import time

def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501, plot_data=0):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT)                                         # Nanonis TCP interface
    try:
        bspec = BiasSpectr(NTCP)                                                # Nanonis TCP Bias Spectroscopy Module
        
        """
        Open
        """
        bspec.Open()
        print("Bias Spectroscopy module open")
        print("----------------------------------------------------------------------")
        
        """
        Start
        """
        data_dict,parameters = bspec.Start(get_data=1,save_base_name="NTCP-Test-")
        if(plot_data):
            import matplotlib.pyplot as plt
            plt.plot(data_dict['Bias calc (V)'],data_dict['Current (A)'])
        print("data channels: " + str(data_dict.keys()))
        print("parameters:    " + str(parameters))
        print("----------------------------------------------------------------------")
        
        """
        Stop
        """
        bspec.Stop()
        print("Stopped spec")
        print("----------------------------------------------------------------------")
        
        """
        Status Get
        """
        status = bspec.StatusGet()
        print("Status: " + ["Not running","Running"][status])
        print("----------------------------------------------------------------------")
        
        """
        ChsSet/Get
        """
        
    except:
        print(traceback.format_exc())
        
    NTCP.close_connection()
    return print('end of test')
        
