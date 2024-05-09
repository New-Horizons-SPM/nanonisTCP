# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 08:41:34 2023

@author: jced0001
"""
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!WARNING: RUNNING run_test() WILL CHANGE SETTINGS IN NANONIS. RUN IT ON A SIM!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
import time
from nanonisTCP import nanonisTCP
from nanonisTCP.Osci2T import Osci2T
import traceback

def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501, plotData=1, debug=False, version=13520):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT, version=version)                        # Nanonis TCP interface
    try:
        osci2T = Osci2T(NTCP)                                                   # Nanonis TCP Oscilloscope 2-Channels Module
        """
        Osci2T Run
        """
        osci2T.Run()
        if(debug):
            print("Osci2T Running")
            print("----------------------------------------------------------------------")
        
        """
        Osci2T ChsSet/Get
        """
        osci2T.ChsSet(chA=0,chB=24)
        chA,chB = osci2T.ChsGet()
        if(debug):
            print("Channel A Index: ",chA)
            print("Channel B Index: ",chB)
            print("----------------------------------------------------------------------")
        
        """
        Osci2T TimebaseSet/Get
        """
        osci2T.TimebaseSet(timebaseIndex=5)
        timebaseIndex,timebases = osci2T.TimebaseGet()
        if(debug):
            print("timebaseIndex: ",timebaseIndex)
            print("timebases: ",timebases)
            print("----------------------------------------------------------------------")
        
        """
        Oversample Set/Get
        """
        osci2T.OversamplSet(oversamplingIndex=4)
        oversamplingIndex = osci2T.OversamplGet()
        if(debug):
            print("Oversampling Index",oversamplingIndex)
            print("----------------------------------------------------------------------")
        
        """
        Trig Set/Get
        """
        time.sleep(1)                                                           # Updating trigger too soon sometimes causes Nanonis not to register for some reason?
        osci2T.TrigSet(mode=0, channel=0, slope=1, level=0, hysteresis=0, position=2)
        mode,channel,slope,level,hysteresis,position = osci2T.TrigGet()
        if(debug):
            print("Mode",mode)
            print("Channel",channel)
            print("slope",slope)
            print("level",level)
            print("hysteresis",hysteresis)
            print("position",position)
            print("----------------------------------------------------------------------")
        
        """
        DataGet
        """
        time.sleep(2) # Wait for data
        t0,dt,chA,chB = osci2T.DataGet(dataToGet=0)
        if(plotData):
            import matplotlib.pyplot as plt
            import numpy as np
            xx = np.arange(len(chA))*dt + t0
            plt.plot(xx,chA)
            plt.plot(xx,chB)
            
        
    except:
        NTCP.close_connection()
        return traceback.format_exc()
        
    NTCP.close_connection()
    return "success"