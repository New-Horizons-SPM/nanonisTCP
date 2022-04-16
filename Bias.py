# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 15:39:58 2022

@author: jced0001
"""

class Bias:
    """
    Nanonis Bias Module
    """
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def Set(self, bias):
        """
        Set the tip voltage bias

        Parameters
        bias (float32): bias (V)
        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Bias.Set', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(bias)                         # bias (float 32)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def Get(self):
        """
        Returns the tip bias

        Returns
        bias (float32): bias (V)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Bias.Get', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        bias = self.NanonisTCP.hex_to_float32(response[0:4].hex())
        return bias