# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 13:33:17 2022

@author: jced0001
"""


from nanonisTCP import nanonisTCP
from nanonisTCP.BiasSpectroscopy import BiasSpectroscopy

def run_test(TCP_IP = '127.0.0.1', TCP_PORT = 6501, make_plot=False):
    """
    Set up the TCP connection and interface
    """
    NTCP = nanonisTCP(TCP_IP, TCP_PORT)                                             # Nanonis TCP interface
    
    biasSpec = BiasSpectroscopy(NTCP)                                               # Nanonis Bias Spectroscopy Module
    
    """
    Open
    """
    biasSpec.Open()
    
    """
    Start/Stop Spectroscopy
    """
    # Start a spectroscopy measurement and wait until it finishes to get the data
    channels_names,data,parameters = biasSpec.Start(get_data=True,save_base_name="spectr_base_name_test")
    if(make_plot):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for i,c in enumerate(channels_names):
            ax.plot(data[i],label=c)
        ax.legend()
    
    # Start a spectrscopy experiment and don't wait until it finishes. then stop it
    import time
    channels_names,data,parameters = biasSpec.Start(get_data=False,save_base_name="spectr_base_name_test")
    time.sleep(3)
    biasSpec.Stop()                                                             # Stop doesn't work when the spectrsocopy was started using the Start function. it does work when spectroscopy is started from pressing play in nanonis?
    
    NTCP.close_connection()