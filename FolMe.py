# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 15:40:21 2022

@author: jced0001
"""

class FolMe:
    """
    Nanonis Follow Me Module
    """
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def XYPosSet(self, X, Y, Wait_end_of_move=False):
        """
        This function moves the tip to the specified X and Y target coordinates
        (in meters). It moves at the speed specified by the "Speed" parameter
        in the Follow Me mode of the Scan Control module. This function will 
        return when the tip reaches its destination or if the movement stops.

        Parameters
        X : Set x position (m)
        Y : Set y position (m)
        Wait_end_of_move : False: Selects whether the function  immediately
                           True: Waits until tip stops moving
        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('FolMe.XYPosSet', body_size=20)
        
        ## arguments
        hex_rep += self.NanonisTCP.float64_to_hex(X)
        hex_rep += self.NanonisTCP.float64_to_hex(Y)
        hex_rep += self.NanonisTCP.to_hex(Wait_end_of_move,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)

    def XYPosGet(self, Wait_for_newest_data):
        """
        Returns the X,Y tip coordinates

        Parameters
        Wait_for_newest_data (uint32): 

        Returns
        xpos : x position of the tip (m)
        ypos : y position of the tip (m)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('FolMe.XYPosGet', body_size=4)
        
        # arguments
        hex_rep += self.NanonisTCP.to_hex(Wait_for_newest_data,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        ## Receive Response
        response = self.NanonisTCP.receive_response(16)
        
        xpos = self.NanonisTCP.hex_to_float64(response[0:8])
        ypos = self.NanonisTCP.hex_to_float64(response[8:16])
        
        return (xpos,ypos)
    
    def SpeedSet(self, speed, custom_speed):
        """
        Configures the tip speed when moving in Follow Me

        Parameters
        speed (float32)       : sets the surface speed in Follow Me
        custom_speed (uint32) : True:  speed setting is custom speed
                                False: speed setting is scan speed
                                
        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('FolMe.SpeedSet', body_size=8)
        
        # arguments
        hex_rep += self.NanonisTCP.float32_to_hex(speed)
        hex_rep += self.NanonisTCP.to_hex(custom_speed,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check for errors)
        self.NanonisTCP.receive_response(0)
    
    def SpeedGet(self):
        """
        Returns the tip speed when moving in Follow Me mode

        Returns
        -------
        speed (float32)       : surface speed in Follow Me mode
        custom_speed (uint32) : True:  speed setting is custom speed
                                False: speed setting is scam speed
                                
        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('FolMe.SpeedGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.NanonisTCP.receive_response(8)
        
        speed        = self.NanonisTCP.hex_to_float32(response[0:4])
        custom_speed = self.NanonisTCP.hex_to_uint32(response[4:8]) > 0
        
        return (speed,custom_speed)
    
    def OversamplSet(self,Oversampling):
        """
        Sets the oversampling of the acquired data when the tip is moving in
        Follow Me mode

        Parameters
        Oversampling (int) : oversampling of data acquisition in fol me mode

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('FolMe.OversamplSet', body_size=4)
        
        # arguments
        hex_rep += self.NanonisTCP.to_hex(Oversampling,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check for errors only)
        self.NanonisTCP.receive_response(0)
    
    def OversamplGet(self):
        """
        Returns the overampling and rate of the acquired data when tip is in
        Follow Me mode

        Returns
        oversampling (int)    : oversampling of data acquisition in fol me mode
        sample_rate (float32) : sample rate

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('FolMe.OversamplGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.NanonisTCP.receive_response(8)
        
        oversampling = self.NanonisTCP.hex_to_int32(response[0:4])
        sample_rate  = self.NanonisTCP.hex_to_float32(response[4:8])
        
        return (oversampling, sample_rate)
    
    def Stop(self):
        """
        Stops the tip movement in follow me mode

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('FolMe.Stop', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)
    
    def PSOnOffSet(self,ps_status):
        """
        Enables or disables Point & Shoot in Follow Me mode

        Parameters
        ps_status (boolean) : True:  enabled
                              False: disabled

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('FolMe.PSOnOffSet', body_size=4)
        
        # arguments
        hex_rep += self.NanonisTCP.to_hex(ps_status,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)
        
    def PSOnOffGet(self):
        """
        Returns if Point & Shoot is enabled or disabled in follow me mode

        Returns
        ps_status (boolean): True:  enabled
                             False: disabled

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('FolMe.PSOnOffGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.NanonisTCP.receive_response(4)
        
        ps_status = self.NanonisTCP.hex_to_uint32(response[0:4]) > 0
        
        return ps_status
    