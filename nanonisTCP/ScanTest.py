# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 12:24:35 2022

@author: jced0001
"""

from nanonisTCP import nanonisTCP
from nanonisTCP.Scan import Scan

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501, make_plot=False):
    
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT)                                             # Nanonis TCP interface
    
    try:
        scan = Scan(NTCP)                                                               # Nanonis Scan Module
        
        """
        Frame Parameters Set/Get
        """
        scan.FrameSet(5e-9,-5e-9,30e-9,30e-9,15)
        x,y,w,h,angle = scan.FrameGet()
        print("Frame Parameters")
        print("Frame Position:  " + str(x) + " m," + str(y) + " m")
        print("Frame dimension: " + str(w) + " m x " + str(h) + " m")
        print("Frame angle:     " + str(angle) + " deg")
        print("----------------------------------------------------------------------")

        """
        Buffer Parameters Set/Get
        """
        scan.BufferSet(channel_indexes=[0,14],pixels=128,lines=128)
        num_channels,channel_indexes,pixels,lines = scan.BufferGet()
        print("Buffer Parameters")
        print("Buffer num_channels:    " + str(num_channels))
        print("Buffer channel_indexes: " + str(channel_indexes))
        print("Buffer pixels:          " + str(pixels))
        print("Buffer lines:           " + str(lines))
        print("----------------------------------------------------------------------")

        """
        Props Set/Get
        """
        scan.PropsSet(bouncy_scan=1,comment="testing123")
        continuous_scan,bouncy_scan,autosave,series_name,comment = scan.PropsGet()
        print("Props Parameters")
        print("Props continuous_scan: " + str(continuous_scan))
        print("Props bouncy_scan:     " + str(bouncy_scan))
        print("Props autosave:        " + str(autosave))
        print("Props series_name:     " + str(series_name))
        print("Props comment:         " + str(comment))
        print("----------------------------------------------------------------------")

        """
        Speed Set/Get
        """
        # Best practice here is to define at least (fwd_speed or fwd_line_time) + (corresponding bwd param or speed_ratio)
        # e.g. one of these...
        # scan.SpeedSet(fwd_speed=150e-9,bwd_speed=400e-9)                              # Expect speeds to be set accordingly and constant param = line speed
        # scan.SpeedSet(fwd_line_time=1,bwd_line_time=0.25)                             # Expect times to be set accordingly and constant param = line time
        # scan.SpeedSet(fwd_speed=150e-9,speed_ratio=2)                                 # Expect fwd_speed=150e-9 and bwd_speed=300e-9
        scan.SpeedSet(fwd_line_time=1,speed_ratio=2)                                    # Expect fwd_line_time=1s and bwd_line_time=0.5s

        fwd_speed,bwd_speed,fwd_line_time,bwd_line_time,const_param,speed_ratio = scan.SpeedGet()
        print("Scan Speed Parameters")
        print("Forward speed:      " + str(fwd_speed))
        print("Backward speed:     " + str(bwd_speed))
        print("Forward line time:  " + str(fwd_line_time))
        print("Backward line time: " + str(bwd_line_time))
        print("Constant Param:     " + ["Constant speed", "Constant time"][const_param])
        print("Speed ratio:        " + str(speed_ratio))
        print("----------------------------------------------------------------------")
        
        
        """
        Action
        """
        scan.Action("start","down")

        """
        Status Get
        """

        """
        Wait end of scan
        """
        timeout_status, file_path_size, file_path = scan.WaitEndOfScan()
        print("Wait end of scan")
        print("timeout_status: " + ["EOS","Timed out"][timeout_status])
        print("file_path: " + file_path)
        print("----------------------------------------------------------------------")
       
        """
        FrameDataGrab
        """
        channel_name,scan_data,scan_direction = scan.FrameDataGrab(14, 1)
        print("Frame Data")
        print("Channel name:   " + channel_name)
        print("Scan direction: " + ["Down","Up"][scan_direction])
        print("Run commented code to show scan_data")
        if make_plot == True:
            import matplotlib.pyplot as plt
            import matplotlib
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.imshow(scan_data)
        print("----------------------------------------------------------------------")

    except:
        print('error')
    
    NTCP.close_connection()

    return print('end of test')