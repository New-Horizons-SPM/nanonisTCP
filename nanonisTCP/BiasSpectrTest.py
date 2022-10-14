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
import numpy as np

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
        data = bspec.Start(get_data=1,save_base_name="NTCP-Test-")
        data_dict  = data['data_dict']
        parameters = data['parameters']
        if(plot_data):
            import matplotlib.pyplot as plt
            plt.plot(data_dict['Bias calc (V)'],data_dict['Current (A)'])
        print("data channels: " + str(data_dict.keys()))
        print("parameters:    " + str(parameters))
        print("----------------------------------------------------------------------")
        
        """
        Stop
        """
        # Cannot test the Stop function like below... the reason is nanonis 
        # server side sends a response back over the initiating port and cannot
        # receive another instruction (i.e. Stop) until the data acquisition is
        # complete (even if get_data=0). This means if you want to start an 
        # acquisition and then stop it before it finishes, you must send the 
        # Stop command on a separate port.
        
        # bspec.Start(get_data=0,save_base_name="NTCP-Test-Stop-")              # Can't do this to test. must be started and stopped on separate ports
        # time.sleep(4)
        
        bspec.Stop()
        print("Acquisition stopped")
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
        channel_indexes = [0,14,16]
        bspec.ChsSet(channel_indexes=channel_indexes,mode="set")
        channel_indexes = bspec.ChsGet()
        print("channels : " + str(channel_indexes))
        print("----------------------------------------------------------------------")
        
        """
        Props Set/Get
        """
        bspec.PropsSet(save_all=1,num_sweeps=20,back_sweep=0,num_points=200,z_offset=10e-12,autosave=0,save_dialog=2)
        propsDict = bspec.PropsGet()
        print("Properties:\n" + str(propsDict))
        print("----------------------------------------------------------------------")
        
        """
        AdvPropsSet/Get
        """
        bspec.AdvPropsSet(reset_bias=0,z_controller_hold=0,record_final_z=0,lockin_run=0)
        advancedProps = bspec.AdvPropsGet()
        print("Advanced Properties:\n" + str(advancedProps))
        print("----------------------------------------------------------------------")
        
        """
        LimitsSet/Get
        """
        bspec.LimitsSet(start_value=-1.1,end_value=1.1)
        limits = bspec.LimitsGet()
        print("Spec limits:\n" + str(limits))
        print("----------------------------------------------------------------------")
        
        """
        TimingSet/Get
        """
        # Note: minimum times are 50us. anything lower than this will either 
        # round up to 50us or down to 0s
        bspec.TimingSet(z_averaging_time=51e-5,z_offset=1.2e-9,initial_settling_time=370e-6,maximum_slew_rate=np.inf,settling_time=12e-6,integration_time=57e-6,end_settling_time=91e-6,z_control_time=61e-6)
        timing = bspec.TimingGet()
        print("Spec Timing:\n" + str(timing))
        print("----------------------------------------------------------------------")
        
        """
        AltZCtrlSet/Get
        """
        bspec.AltZCtrlSet(alternate_setpoint_onoff=1,setpoint=22e-12,settling_time=60e-3)
        altZParams = bspec.AltZCtrlGet()
        print("Spec AltZParams:\n" + str(altZParams))
        print("----------------------------------------------------------------------")
        
        """
        MLSLockinPerSegSet/Get and MLSModeSet/Get
        """
        # This test will fail if sweep mode is not explicitly set to 
        # Multi Segment first.
        bspec.MLSModeSet(sweep_mode="MLS")
        sweep_mode = bspec.MLSModeGet()
        print("Sweep mode: " + sweep_mode)
        bspec.MLSLockinPerSegSet(lockin_per_segment=0)
        lockin_per_segment = bspec.MLSLockinPerSegGet()
        print("Spec lockin per segment: " + ["off","on"][lockin_per_segment])
        print("----------------------------------------------------------------------")
        
        """
        MLSValsSet/Get
        """
        bias_start = [-2,-1]
        bias_end   = [1,2]
        initial_settling_time = [10e-3,12e-3]
        settling_time = [14e-3,16e-3]
        integration_time = [18e-3,20e-3]
        steps = [10,20]
        lockin_run=[0,0]
        bspec.MLSValsSet(bias_start,bias_end,initial_settling_time,settling_time,integration_time,steps,lockin_run)
        mlsVals = bspec.MLSValsGet()
        print("MLS Values:\n" + str(mlsVals))
        print("Setting sweep mode back to Linear...")
        bspec.MLSModeSet(sweep_mode="Linear")
        sweep_mode = bspec.MLSModeGet()
        print("Sweep mode: " + sweep_mode)
        print("----------------------------------------------------------------------")
    except:
        print(traceback.format_exc())
        
    NTCP.close_connection()
    return print('end of test')
        
