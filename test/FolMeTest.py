# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 15:26:23 2022

@author: Julian Ceddia
"""
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!WARNING: RUNNING run_test() WILL CHANGE SETTINGS IN NANONIS. RUN IT ON A SIM!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""


from nanonisTCP import nanonisTCP
from nanonisTCP.FolMe import FolMe
import traceback

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501, debug=False, version=13520):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT, version=version)                                # Nanonis TCP interface
    try:
        followme = FolMe(NTCP)                                                          # Nanonis Follow Me Module

        """
        XYPos Set/Get
        """
        followme.XYPosSet(5e-9, -5e-9, Wait_end_of_move=True)                           # Set xy pos to 5 nm, -5 nm
        x,y = followme.XYPosGet(Wait_for_newest_data=True)                              # Get the current XY tip position
        if(debug):
            print("Tip Position: " + str(x) + " m, " + str(y) + " m")    

        """
        Speed Set/Get
        """
        followme.SpeedSet(speed=100e-9, custom_speed=True)                              # Set the custom move speed to 100 nm/s. Set move mode to custom speed
        speed, custom_speed = followme.SpeedGet()                                       # Get the custom move speed. get the mode
        if(debug):
            print("Speed: " + str(speed) + " m/s")
            print("Mode: " + ["Scan Speed","Custom Speed"][custom_speed])

        """
        Oversampl Set/Get
        """
        followme.OversamplSet(3)                                                        # Set the oversampling for data acquisition in follow me mode
        oversample, sample_rate = followme.OversamplGet()                               # Get the oversampling and sample rate for data acquisition in follow me mode
        if(debug):
            print("Oversampling: " + str(oversample) + " @ " + str(sample_rate) + "S/s")

        """
        Stop
        """
        followme.Stop()                                                                 # Stop the tip from moving. no effect if tip position was set with Wait_end_of_move = True

        """
        Point and Shoot Set/Get
        """
        followme.PSOnOffSet(False)                                                      # Disable point and shoot in follow me mode
        ps_status = followme.PSOnOffGet()                                               # Get point and shoot status
        if(debug):
            print("Point & Shoot: " + ["disabled","enabled"][ps_status])
    except:
        NTCP.close_connection()
        return(traceback.format_exc())

    NTCP.close_connection()
    return "success"
