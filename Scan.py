# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 09:33:32 2022

@author: jced0001
"""

class Scan:
    """
    Nanonis Scan Module
    """
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
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
        hex_rep = self.NanonisTCP.make_header('Scan.Action', body_size=6)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(action_dict[scan_action],2)
        hex_rep += self.NanonisTCP.to_hex(action_dict[scan_direction],4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)
    
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
        hex_rep = self.NanonisTCP.make_header('Scan.WaitEndOfScan', body_size=4)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(timeout,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.NanonisTCP.receive_response()
        
        timeout_status = self.NanonisTCP.hex_to_uint32(response[0:4]) > 0
        file_path_size = self.NanonisTCP.hex_to_uint32(response[4:8])
        file_path      = response[8:8+file_path_size].decode()
        
        self.NanonisTCP.check_error(response, 8+file_path_size)
        
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
        hex_rep = self.NanonisTCP.make_header('Scan.FrameSet', body_size=20)
        
        ## arguments
        hex_rep += self.NanonisTCP.float32_to_hex(x)
        hex_rep += self.NanonisTCP.float32_to_hex(y)
        hex_rep += self.NanonisTCP.float32_to_hex(w)
        hex_rep += self.NanonisTCP.float32_to_hex(h)
        hex_rep += self.NanonisTCP.float32_to_hex(angle)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)
        
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
        hex_rep = self.NanonisTCP.make_header('Scan.FrameGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.NanonisTCP.receive_response(20)
        
        x     = self.NanonisTCP.hex_to_float32(response[0:4])
        y     = self.NanonisTCP.hex_to_float32(response[4:8])
        w     = self.NanonisTCP.hex_to_float32(response[8:12])
        h     = self.NanonisTCP.hex_to_float32(response[12:16])
        angle = self.NanonisTCP.hex_to_float32(response[16:20])
        
        return [x,y,w,h,angle]
    
    def BufferSet(self,channel_indexes,pixels,lines):
        """
        Configures the scan buffer parameters

        Parameters
        num_channels    : number of recorded channels.
        channel_indexes : indexes of recorded channels (see signals manager or
                          use Signals.InSlotsGet function)
        pixels          : number of pixels per line. forced to a multiple of 16
        lines           : number of scan lines

        """
        num_channels = len(channel_indexes)
        body_size    = 12 + 4*num_channels                                      # Variable body size depending on number of channels. each channel index is a float32 thus 4 bytes
        
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Scan.BufferSet', body_size=body_size)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(num_channels,4)
        for c in channel_indexes:
            hex_rep += self.NanonisTCP.to_hex(c,4)
        hex_rep += self.NanonisTCP.to_hex(pixels,4)
        hex_rep += self.NanonisTCP.to_hex(lines,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)
        
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
        hex_rep = self.NanonisTCP.make_header('Scan.BufferGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.NanonisTCP.receive_response()
        
        idx = 0
        channel_indexes = []
        num_channels = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        for c in range(num_channels):
            idx += 4
            channel_indexes.append(self.NanonisTCP.hex_to_int32(response[idx:idx+4]))
        
        idx += 4
        pixels = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        
        idx += 4
        lines = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        
        # Receive Response (check errors)
        idx += 4
        self.NanonisTCP.check_error(response, idx)                              # Makes no sense to check if there's error at this point, but how else do we check?
        
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
        series_name_size = int(len(self.NanonisTCP.string_to_hex(series_name))/2)
        comment_size     = int(len(self.NanonisTCP.string_to_hex(comment))/2)
        body_size = 20 + series_name_size + comment_size
        
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Scan.PropsSet', body_size=body_size)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(continuous_scan,4)
        hex_rep += self.NanonisTCP.to_hex(bouncy_scan,4)
        hex_rep += self.NanonisTCP.to_hex(autosave,4)
        hex_rep += self.NanonisTCP.to_hex(series_name_size,4)
        if(series_name_size > 0):
            hex_rep += self.NanonisTCP.string_to_hex(series_name)
        hex_rep += self.NanonisTCP.to_hex(comment_size,4)
        if(comment_size > 0):
            hex_rep += self.NanonisTCP.string_to_hex(comment)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)