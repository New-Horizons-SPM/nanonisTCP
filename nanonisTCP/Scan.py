# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 09:33:32 2022

@author: jced0001
"""
import numpy as np
class Scan:
    """
    Nanonis Scan Module
    """
    def __init__(self, nanonisTCP):
        self.nanonisTCP = nanonisTCP
    
    def Action(self, scan_action, scan_direction="up"):
        """
        Sarts, stops, pauses, or resumes a scan

        Parameters
        scan_action     : one of "start", "stop", "pause", "resume"
        scan_direction  : "up" or "down"
        
        """
        action_dict = {"start" : 0,
                       "stop"  : 1,
                       "pause" : 2,
                       "resume": 3,
                       "down"  : 0,
                       "up"    : 1
                       }
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Scan.Action', body_size=6)
        
        ## arguments
        hex_rep += self.nanonisTCP.to_hex(action_dict[scan_action],2)
        hex_rep += self.nanonisTCP.to_hex(action_dict[scan_direction],4)
        
        self.nanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.nanonisTCP.receive_response(0)
    
    def WaitEndOfScan(self,timeout=-1):
        """
        Waits for the end-of-scan
        This function returns only when an end-of-scan or timeout occurs (which
        ever occurs first)

        Parameters
        timeout : timeout in ms. if -1, it waits indefinitely

        Returns
        timeout_status : 1: function timed out. 0: didn't time out
        

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Scan.WaitEndOfScan', body_size=4)
        
        ## arguments
        hex_rep += self.nanonisTCP.to_hex(timeout,4)
        
        self.nanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.nanonisTCP.receive_response()
        
        timeout_status = self.nanonisTCP.hex_to_uint32(response[0:4]) > 0
        file_path_size = self.nanonisTCP.hex_to_uint32(response[4:8])
        file_path      = response[8:8+file_path_size].decode()
        
        self.nanonisTCP.check_error(response, 8+file_path_size)
        
        return [timeout_status, file_path_size, file_path]
    
    def FrameSet(self,x,y,w,h,angle=0):
        """
        Configures the scan frame position and dimensions
        
        Parameters
        x     : centre x coordinate
        y     : centre y coordinate
        w     : scan frame width
        h     : scan frame height
        angle : scan frame angle (degrees). angle > 0: clockwise
        
        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Scan.FrameSet', body_size=20)
        
        ## arguments
        hex_rep += self.nanonisTCP.float32_to_hex(x)
        hex_rep += self.nanonisTCP.float32_to_hex(y)
        hex_rep += self.nanonisTCP.float32_to_hex(w)
        hex_rep += self.nanonisTCP.float32_to_hex(h)
        hex_rep += self.nanonisTCP.float32_to_hex(angle)
        
        self.nanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.nanonisTCP.receive_response(0)
        
    def FrameGet(self):
        """
        Returns the scan frame position and dimensions

        Returns
        x     : centre x coordinate
        y     : centre y coordinate
        w     : scan frame width
        h     : scan frame height
        angle : scan frame angle (degrees). angle > 0: clockwise 

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Scan.FrameGet', body_size=0)
        
        self.nanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.nanonisTCP.receive_response(20)
        
        x     = self.nanonisTCP.hex_to_float32(response[0:4])
        y     = self.nanonisTCP.hex_to_float32(response[4:8])
        w     = self.nanonisTCP.hex_to_float32(response[8:12])
        h     = self.nanonisTCP.hex_to_float32(response[12:16])
        angle = self.nanonisTCP.hex_to_float32(response[16:20])
        
        return [x,y,w,h,angle]
    
    def BufferSet(self,channel_indexes=None,pixels=None,lines=None):
        """
        Configures the scan buffer parameters

        Parameters
        num_channels    : number of recorded channels.
        channel_indexes : indexes of recorded channels (see signals manager or
                          use Signals.InSlotsGet function)
        pixels          : number of pixels per line. forced to a multiple of 16
        lines           : number of scan lines

        """
        _, buf_channel_indexes, buf_pixels, buf_lines = self.BufferGet()        # Get the values currently in the buffer
        
        if(not channel_indexes): channel_indexes = buf_channel_indexes          # Keep the original value if we don't want to change it in this call
        if(not pixels):          pixels = buf_pixels                            # Keep the original value if we don't want to change it in this call
        if(not lines):           lines = buf_lines                              # Keep the original value if we don't want to change it in this call
            
        num_channels = len(channel_indexes)                                     # num_channels is needed as an argument
        body_size    = 12 + 4*num_channels                                      # Variable body size depending on number of channels. each channel index is a float32 thus 4 bytes
        
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Scan.BufferSet', body_size=body_size)
        
        ## arguments
        hex_rep += self.nanonisTCP.to_hex(num_channels,4)
        for c in channel_indexes:
            hex_rep += self.nanonisTCP.to_hex(c,4)
        hex_rep += self.nanonisTCP.to_hex(pixels,4)
        hex_rep += self.nanonisTCP.to_hex(lines,4)
        
        self.nanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.nanonisTCP.receive_response(0)
        
    def BufferGet(self):
        """
        Returns the scan buffer parameters

        Returns
        num_channels    : number of recorded channels.
        channel_indexes : indexes of recorded channels (see signals manager or
                          use Signals.InSlotsGet function)
        pixels          : number of pixels per line. forced to a multiple of 16
        lines           : number of scan lines

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Scan.BufferGet', body_size=0)
        
        self.nanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.nanonisTCP.receive_response()
        
        idx = 0
        channel_indexes = []
        num_channels = self.nanonisTCP.hex_to_int32(response[idx:idx+4])
        for c in range(num_channels):
            idx += 4
            channel_indexes.append(self.nanonisTCP.hex_to_int32(response[idx:idx+4]))
        
        idx += 4
        pixels = self.nanonisTCP.hex_to_int32(response[idx:idx+4])
        
        idx += 4
        lines = self.nanonisTCP.hex_to_int32(response[idx:idx+4])
        
        # Receive Response (check errors)
        idx += 4
        self.nanonisTCP.check_error(response, idx)                              # Makes no sense to check if there's error at this point, but how else do we check?
        
        return [num_channels,channel_indexes,pixels,lines]
        
    def PropsSet(self,continuous_scan=0,bouncy_scan=0,autosave=0,series_name="%y%m%d_%H-%M-%S_SPM",comment=""):
        """
        Configures some of the scan parameters

        Parameters
        continuous_scan : sets whether the scan continues or stops when a frame
                          has been completed.
                          0: no change (leave previous setting)
                          1: turn on
                          2: turn off
                          
        bouncy_scan     : sets whether the scan direction changes when a frame
                          has been completed.
                          0: no change (leave previous setting)
                          1: turn on (scan direction changes each EOS)
                          2: turn off (scan direction doesn't change each EOS)
            
        autosave        : defines the save behaviour when a frame has been
                          completed.
                          0: no change (leave previous setting)
                          1: save all
                          2: save next only
                          3: turn off (save none)
        series_name     : is the base name used for the saved images
        
        comment         : is the comment saved in the file

        """
        series_name_size = int(len(self.nanonisTCP.string_to_hex(series_name))/2)
        comment_size     = int(len(self.nanonisTCP.string_to_hex(comment))/2)
        body_size = 20 + series_name_size + comment_size
        
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Scan.PropsSet', body_size=body_size)
        
        ## arguments
        hex_rep += self.nanonisTCP.to_hex(continuous_scan,4)
        hex_rep += self.nanonisTCP.to_hex(bouncy_scan,4)
        hex_rep += self.nanonisTCP.to_hex(autosave,4)
        hex_rep += self.nanonisTCP.to_hex(series_name_size,4)
        if(series_name_size > 0):
            hex_rep += self.nanonisTCP.string_to_hex(series_name)
        hex_rep += self.nanonisTCP.to_hex(comment_size,4)
        if(comment_size > 0):
            hex_rep += self.nanonisTCP.string_to_hex(comment)
        
        self.nanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.nanonisTCP.receive_response(0)
        
    def PropsGet(self):
        """
        Returns some of the scan parameters
        
        Returns
        continuous_scan : sets whether the scan continues or stops when a frame
                          has been completed.
                          0: off
                          1: on
                          
        bouncy_scan     : sets whether the scan direction changes when a frame
                          has been completed.
                          0: off (scan direction doesn't change each EOS)
                          1: on (scan direction changes each EOS)
            
        autosave        : defines the save behaviour when a frame has been
                          completed.
                          0: save all
                          1: save next only
                          2: off (save none)
        series_name     : is the base name used for the saved images
        
        comment         : is the comment saved in the file

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Scan.PropsGet', body_size=0)
        
        self.nanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.nanonisTCP.receive_response()
        
        continuous_scan = self.nanonisTCP.hex_to_uint32(response[0:4])
        bouncy_scan     = self.nanonisTCP.hex_to_uint32(response[4:8])
        autosave        = self.nanonisTCP.hex_to_uint32(response[8:12])
        
        series_name = ""
        series_name_size = self.nanonisTCP.hex_to_int32(response[12:16])
        if(series_name_size > 0):
            series_name = response[16:16+series_name_size].decode()
        
        comment = ""
        idx = 16+series_name_size
        comment_size = self.nanonisTCP.hex_to_int32(response[idx:idx+4])
        if(comment_size > 0):
            idx += 4
            comment = response[idx:idx+comment_size].decode()
        
        return [continuous_scan,bouncy_scan,autosave,series_name,comment]
        
    def SpeedSet(self,fwd_speed=0,bwd_speed=0,fwd_line_time=0,bwd_line_time=0,const_param=-1,speed_ratio=0):
        """
        Configures the scan speed parameters. Best practice here is to define
        at least (fwd_speed or fwd_line_time)
               + (corresponding bwd param or speed_ratio)
               
        e.g like one of these:
            
            SpeedSet(fwd_speed=150e-9,bwd_speed=400e-9)
            SpeedSet(fwd_line_time=1,bwd_line_time=0.25)
            SpeedSet(fwd_speed=150e-9,speed_ratio=2)
            SpeedSet(fwd_line_time=1,speed_ratio=2)
        
        Parameters
        fwd_speed       : forward linear speed (m/s)
        bwd_speed       : backward linear speed (m/s)
        fwd_line_time   : forward time per line
        bwd_line_time   : backward time per line
        const_param     : defines which speed parameter to keep constant
                          0: No change (leave setting as is)
                          1: keeps linear speed constant
                          2: keeps time per line constant
        speed_ratio     : defines the backward tip speed relative to the
                          forward tip speed

        """
        buf_fwd_speed, buf_bwd_speed, buf_fwd_line_time, buf_bwd_line_time, buf_const_param, buf_speed_ratio = self.SpeedGet()
        
        if(const_param < 0):                                                    # If const_param is not provided, figure out what it should be based on inputs
            if(fwd_speed and not fwd_line_time):  const_param = 1               # If speed is provided and time is not, then assume we want to set speed
            if(not fwd_speed and fwd_line_time):  const_param = 2               # If time is provided and speed is not, then assume we want to set time
        
        if(const_param < 0):
            if(bwd_speed and not bwd_line_time):  const_param = 1               # If speed is provided and time is not, then assume we want to set speed
            if(not bwd_speed and bwd_line_time):  const_param = 2               # If time is provided and speed is not, then assume we want to set time
                        
        if(bwd_speed and fwd_speed and not speed_ratio):                        # If bwd_speed and fwd_speed have been provided, then set the speed_ratio.)
            speed_ratio = bwd_speed/fwd_speed                                   # Nanonis Speed module seems to do literally nothing with the bwd parameters... it just used the speed_ratio to calc bwd from fwd
        
        if(bwd_line_time and fwd_line_time and not speed_ratio):                # If bwd_line_time and fwd_line_time have been provided...
            speed_ratio = fwd_line_time/bwd_line_time                           # then set the speed ratio similar to above. If speed and time have been provided then the ratio is calculated based on time
        
        # Could add more functionality here to accommodate for other combinations of inputs. Not going to do that unless necessary
        
        if(not fwd_speed):      fwd_speed     = buf_fwd_speed
        if(not bwd_speed):      bwd_speed     = buf_bwd_speed
        if(not fwd_line_time):  fwd_line_time = buf_fwd_line_time
        if(not bwd_line_time):  bwd_line_time = buf_bwd_line_time
        if(not speed_ratio):    speed_ratio   = buf_speed_ratio
        
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Scan.SpeedSet', body_size=22)
        
        ## arguments
        hex_rep += self.nanonisTCP.float32_to_hex(fwd_speed)
        hex_rep += self.nanonisTCP.float32_to_hex(bwd_speed)
        hex_rep += self.nanonisTCP.float32_to_hex(fwd_line_time)
        hex_rep += self.nanonisTCP.float32_to_hex(bwd_line_time)
        hex_rep += self.nanonisTCP.to_hex(const_param,2)
        hex_rep += self.nanonisTCP.float32_to_hex(speed_ratio)
        
        self.nanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.nanonisTCP.receive_response(0)
        
    def SpeedGet(self):
        """
        Returns the scan speed parameters

        Returns
        fwd_speed       : forward linear speed (m/s)
        bwd_speed       : backward linear speed (m/s)
        fwd_line_time   : forward time per line
        bwd_line_time   : backward time per line
        const_param     : defines which speed parameter to keep constant
                          0: No change (leave setting as is)
                          1: keeps linear speed constant
                          2: keeps time per line constant
        speed_ratio     : defines the backward tip speed relative to the
                          forward tip speed

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Scan.SpeedGet', body_size=0)
        
        self.nanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.nanonisTCP.receive_response()
        
        fwd_speed     = self.nanonisTCP.hex_to_float32(response[0:4])
        bwd_speed     = self.nanonisTCP.hex_to_float32(response[4:8])
        fwd_line_time = self.nanonisTCP.hex_to_float32(response[8:12])
        bwd_line_time = self.nanonisTCP.hex_to_float32(response[12:16])
        const_param   = self.nanonisTCP.hex_to_uint16(response[16:18])
        speed_ratio   = self.nanonisTCP.hex_to_float32(response[18:22])
        
        return [fwd_speed,bwd_speed,fwd_line_time,bwd_line_time,const_param,speed_ratio]
    
    def FrameDataGrab(self,channel_index,data_direction):
        """
        Returns the scan data of the selected frame

        Parameters
        channel_index   : selects which channel to get the data from. The 
                          channel must be one of the acquired channels. The 
                          list of acquired channels while scanning can be 
                          configured by the function Scan.BufferSet or read by
                          the function Scan.BufferGet
        data_direction : selects the data direction to be read.
                         0: backward
                         1: forward

        Returns
        -------
        None.

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Scan.FrameDataGrab', body_size=8)
        
        ## arguments
        hex_rep += self.nanonisTCP.to_hex(channel_index,4)
        hex_rep += self.nanonisTCP.to_hex(data_direction,4)
        
        self.nanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.nanonisTCP.receive_response()
        
        idx = 0
        channel_name_size = self.nanonisTCP.hex_to_int32(response[idx:idx+4])
        
        idx += 4
        channel_name = response[idx:idx+channel_name_size].decode()
        
        idx += channel_name_size
        scan_data_rows = self.nanonisTCP.hex_to_int32(response[idx:idx+4])
        
        idx += 4
        scan_data_columns = self.nanonisTCP.hex_to_int32(response[idx:idx+4])
        
        scan_data = np.empty((scan_data_rows,scan_data_columns))
        for i in range(scan_data_rows):
            for j in range(scan_data_columns):
                idx += 4
                scan_data[i,j] = self.nanonisTCP.hex_to_float32(response[idx:idx+4])
            
        idx += 4
        scan_direction = self.nanonisTCP.hex_to_int32(response[idx:idx+4])
        scan_direction = ["down","up"][scan_direction]
        
        return [channel_name,scan_data,scan_direction]