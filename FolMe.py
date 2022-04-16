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
        
        xpos = self.NanonisTCP.hex_to_float64(response[0:8].hex())
        ypos = self.NanonisTCP.hex_to_float64(response[8:16].hex())
        
        return (xpos,ypos)