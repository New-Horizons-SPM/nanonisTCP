# -*- coding: utf-8 -*-
"""
Created on Thu May  5 11:14:19 2022

@author: Benjamin Lowe
"""
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!WARNING: RUNNING run_test() WILL CHANGE SETTINGS IN NANONIS. RUN IT ON A SIM!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

from nanonisTCP import nanonisTCP
from nanonisTCP.TipShaper import TipShaper
import traceback

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501, make_plot=False, debug=False, version=13520):
    
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT, version=version)                        # Nanonis TCP interface
    
    tipShaper = TipShaper(NTCP)                                                 # Nanonis Tip Shaper Module
    
    try:
              
        """
        Properties Set/Get
        """
        tipShaper.PropsSet(Switch_off_delay=1,Change_bias=1,Bias=0.02,Tip_lift=-2e-9,Lift_time_1=0.2,Bias_lift=0.05,
                Bias_settling_time=0.1,Lift_height=5e-9,Lift_time_2=0.2,End_wait_time=0.1,
                Restore_feedback=1)
        
        Switch_off_delay,Change_bias,Bias,Tip_lift,Lift_time_1,Bias_lift,Bias_settling_time,Lift_height,Lift_time_2,End_wait_time,Restore_feedback = tipShaper.PropsGet()
        if(debug):
            print("Tip Shaper Properties")
            print("Switch off delay:  " + "%f" % Switch_off_delay)
            print("Change Bias status:" + ["no change","True","False"][Change_bias])
            print("Bias: %f" % Bias)
            print("Tip Lift: %f m" % Tip_lift)
            print("Lift_time_1: %f s" % Lift_time_1)
            print("Bias_lift: %f V" % Bias_lift)
            print("Bias settling time: %f s" % Bias_settling_time)
            print("Lift_height: %f m" % Lift_height)
            print("Lift_time_2: %f s" % Lift_time_2)
            print("End_wait_time: %f" % End_wait_time)
            print("Restore Feedback? " + ["no change","yes","no"][Restore_feedback])
            print("----------------------------------------------------------------------")
        
        """
        Start
        """
        tipShaper.Start(wait_until_finished=1,timeout=10)
        
    except:
        NTCP.close_connection()
        return(traceback.format_exc())
    
    NTCP.close_connection()
    return "success"