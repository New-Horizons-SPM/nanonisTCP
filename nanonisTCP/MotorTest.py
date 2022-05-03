# -*- coding: utf-8 -*-
"""
Created on Tue May  3 19:34:49 2022

@author: Julian
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
        motor.StartMove(direction="Z+",steps=10,group=1,wait_until_finished=True)
    except Exception as e:
        print(e)
    
    NTCP.close_connection()