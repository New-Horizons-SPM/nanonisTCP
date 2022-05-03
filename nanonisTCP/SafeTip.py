# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:13:02 2022

@author: jced0001
"""

class SafeTip:
    """
    Nanonis Z-Controller Module
    """
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def OnOffSet(self,safe_tip_status):
        """
        Switches the Safe Tip feature on or off

        Parameters
        ----------
        safe_tip_status : sets the Safe Tip feature on or off
                          0: No change (leave setting as is in nanonis)
                          1: Safe Tip feature on
                          2: Safe Tip feature off

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('SafeTip.OnOffSet', body_size=2)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(safe_tip_status,2)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def OnOffGet(self):
        """
        Returns the Safe Tip feature status (on/off)

        Returns
        -------
        safe_tip_status : sets the Safe Tip feature on or off
                          True:  Safe Tip feature on
                          False: Safe Tip feature off

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('SafeTip.OnOffGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(2)
        
        safe_tip_status = self.NanonisTCP.hex_to_uint16(response[0:2])
        
        return safe_tip_status
    
    def SignalGet(self):
        """
        Returns the current Safe Tip signal value

        Returns
        -------
        signal_value : signal value

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('SafeTip.SignalGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        signal_value = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return signal_value
    
    def PropsSet(self,auto_recovery,auto_pause_scan,threshold):
        """
        Sets the safe tip configuration

        Parameters
        ----------
        auto_recovery   : indicates if Z-Controller automatically recovers from
                          a SafeTip situation after a specified amount of time 
                          if Z-Controller was originall on.
                          False: Off
                          True:  On
        auto_pause_scan : indicates if the Z-Controller automatically pauses/
                          holds the scan on a SafeTip event.
                          False: Off
                          True:  On
        threshold       : defines the condition to trigger the Safe Tip
        
        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('SafeTip.PropsSet', body_size=8)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(auto_recovery,2)
        hex_rep += self.NanonisTCP.to_hex(auto_pause_scan,2)
        hex_rep += self.NanonisTCP.float32_to_hex(threshold)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def PropsGet(self):
        """
        Returns the Safe Tip configuration

        Returns
        -------
        auto_recovery   : indicates if Z-Controller automatically recovers from
                          a SafeTip situation after a specified amount of time 
                          if Z-Controller was originall on.
                          False: Off
                          True:  On
        auto_pause_scan : indicates if the Z-Controller automatically pauses/
                          holds the scan on a SafeTip event.
                          False: Off
                          True:  On
        threshold       : defines the condition to trigger the Safe Tip

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('SafeTip.PropsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(8)
        
        auto_recovery   = self.NanonisTCP.hex_to_uint16(response[0:2])
        auto_pause_scan = self.NanonisTCP.hex_to_uint16(response[2:4])
        threshold       = self.NanonisTCP.hex_to_float32(response[4:8])
        
        return [auto_recovery,auto_pause_scan,threshold]