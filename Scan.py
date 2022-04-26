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
            hex_rep += self.NanonisTCP.float32_to_hex(c)
        hex_rep += self.NanonisTCP.to_hex(pixels,4)
        hex_rep += self.NanonisTCP.to_hex(lines,4)
        
        print(self.NanonisTCP.to_hex(pixels,4))
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)
        