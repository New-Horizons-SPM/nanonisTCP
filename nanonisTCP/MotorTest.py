# -*- coding: utf-8 -*-
"""
Created on Tue May  3 19:34:49 2022

@author: Julian Ceddia
"""
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!WARNING: RUNNING run_test() WILL CHANGE SETTINGS IN NANONIS. RUN IT ON A SIM!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

from nanonisTCP import nanonisTCP
from nanonisTCP.Motor import Motor

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6502, make_plot=False):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT)                                         # Nanonis TCP interface
    
    motor = Motor(NTCP)                                                         # Nanonis Coarse Motion (Motor)Module
    
    try:
        """
        Start Move
        """
        motor.StartMove(direction="Z+",steps=100,group=2,wait_until_finished=False)
        
        """
        Stop Moter Move
        """
        motor.StopMove()
        
        print("----------------------------------------------------------------------")
        """
        Start Closed Loop
        """
        try:
            motor.StartClosedLoop(abs_rel=True, target_x=0, target_y=0, target_z=10, wait_until_finished=False)
        except Exception as e:
            print("Error in Motor.StartClosedLoop: ")
            print(e)
            print("----------------------------------------------------------------------")
        """
        Motor Pos Get
        """
        try:
            x_pos,y_pos,z_pos = motor.PosGet()
            print("Motor Positions")
            print("x pos: " + str(x_pos))
            print("y pos: " + str(y_pos))
            print("z pos: " + str(z_pos))
            print("----------------------------------------------------------------------")
        except Exception as e:
            print("Error in Motor.PosGet: ")
            print(e)
            print("----------------------------------------------------------------------")
        
        """
        Step Counter Get
        """
        try:
            counter_x,counter_y,counter_z = motor.StepCounterGet()
            print("Motor Step Counters")
            print("x steps: " + str(counter_x))
            print("y steps: " + str(counter_y))
            print("z steps: " + str(counter_z))
            print("----------------------------------------------------------------------")
        except Exception as e:
            print("Error in Motor.StepCounterGet: ")
            print(e)
            print("----------------------------------------------------------------------")
        
        """
        Freq/Amp Set/Get
        """
        motor.FreqAmpSet(frequency=1111, amplitude=199)
        [frequency,amplitude] = motor.FreqAmpGet()
        print("Motor Frequency/Amplidtude")
        print("Frequency: " + str(frequency))
        print("Amplitude: " + str(amplitude))
        print("----------------------------------------------------------------------")
        
        print("test complete")
    except Exception as e:
        print(e)
    
    NTCP.close_connection()