# -*- coding: utf-8 -*-
"""
Created on Tue May  3 19:04:05 2022

@author: Julian
"""

class AutoApproach:
    """
    Nanonis Auto Approach Module
    """
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def Open(self):
        """
        Opens the Auto Approach module

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('AutoApproach.Open', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def OnOffSet(self,on_off):
        """
        Starts or stops the Z auto-approach procedure

        Parameters
        ----------
        on_off : starts or stops Z auto approach
                 False: Stops it
                 True:  Starts it

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('AutoApproach.OnOffSet', body_size=2)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(on_off,2)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def OnOffGet(self):
        """
        Returns the on-off status of the Z auto-approach procedure

        Returns
        -------
        on_off : starts or stops Z auto approach
                 False: Off
                 True:  Running

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('AutoApproach.OnOffGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(2)
        
        on_off = self.NanonisTCP.hex_to_uint16(response[0:2])
        
        return on_off