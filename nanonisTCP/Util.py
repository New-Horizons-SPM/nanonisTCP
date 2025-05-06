# -*- coding: utf-8 -*-
"""
Created on Sat Apr 7 15:39:58 2025

@author: jced0001
"""

class Util:
    """
    Nanonis Utilities Module
    """
    def __init__(self, nanonisTCP):
        self.nanonisTCP = nanonisTCP
    
    def SessionPathSet(self, session_path, save=1):
        """
        Set the Nanonis session path

        Parameters
        session_path (str): Desired session path
        save (uint32): Save the new session path to the settings file
        """
        ## Make Header
        session_path_size = int(len(self.nanonisTCP.string_to_hex(session_path))/2)

        hex_rep = self.nanonisTCP.make_header('Util.SessionPathSet', body_size=8 + session_path_size)
        print(session_path_size)
        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(session_path_size,4)
        hex_rep += self.nanonisTCP.string_to_hex(session_path)
        if(save):
            hex_rep += self.nanonisTCP.to_hex(1,4)
        else:
            hex_rep += self.nanonisTCP.to_hex(0,4)

        
        self.nanonisTCP.send_command(hex_rep)
        
        self.nanonisTCP.receive_response(0)
    
    def SessionPathGet(self):
        """
        Returns the Nanonis session path

        Returns
        session_path (str): Current Nanonis session path

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('Util.SessionPathGet', body_size=0)
        
        self.nanonisTCP.send_command(hex_rep)
        
        response = self.nanonisTCP.receive_response()
        
        session_path_size = self.nanonisTCP.hex_to_int32(response[0:4])
        session_path      = response[4:4+session_path_size].decode()
        
        return session_path