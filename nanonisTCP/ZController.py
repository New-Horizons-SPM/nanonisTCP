# -*- coding: utf-8 -*-
"""
Created on Mon May  2 15:32:25 2022

@author: jced0001
"""

class ZController:
    """
    Nanonis BZ-Controller Module
    """
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def ZPosSet(self,zpos):
        """
        Sets the Z position of the tip

        Parameters
        ----------
        zpos : Z position (m)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.ZPosSet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(zpos)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def ZPosGet(self):
        """
        Returns the current Z position of the tip

        Returns
        -------
        zpos : the current z position of the tip

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.ZPosGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        zpos = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return zpos
    
    def OnOffSet(self,on):
        """
        Switches the Z-Controller On or Off

        Parameters
        ----------
        on : True:  turn controller on
             False: turn controller off

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.OnOffSet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(on,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def OnOffGet(self):
        """
        Returns the status of the Z-Controller
        
        Returns
        -------
        z_status : indicates if the controller is on or off
                   True:  Z-Controller is on
                   False: Z-Controller is off
                   
        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.OnOffGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        z_status = self.NanonisTCP.hex_to_uint32(response[0:4])
        
        return z_status
    
    def SetpntSet(self,setpoint):
        """
        Sets the stpoint of the Z-Controller

        Parameters
        ----------
        setpoint : setpoint of the z-controller (A)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.SetpntSet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(setpoint)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def SetpntGet(self):
        """
        Returns the setpoint current of the Z-Controller

        Returns
        -------
        setpoint : setpoint current of the z-controller (A)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.SetpntGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        setpoint = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return setpoint
    
    def GainSet(self,p_gain,time_constant):
        """
        Sets the Z-Controller gains (P,I) and time settings

        Parameters
        ----------
        p_gain        : proportional gain of the regulation loop
        time_constant : time constant of the regulation loop
        i_gain        : integral gain of the regulation loop (I=P/T) (not used)

        """
        i_gain = p_gain/time_constant
        
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.GainSet', body_size=12)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(p_gain)
        hex_rep += self.NanonisTCP.float32_to_hex(time_constant)
        hex_rep += self.NanonisTCP.float32_to_hex(i_gain)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def GainGet(self):
        """
        Returns the Z-Controller gains (P,I) and time constant

        Returns
        -------
        None.

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.GainGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        p_gain        = self.NanonisTCP.hex_to_float32(response[0:4])
        time_constant = self.NanonisTCP.hex_to_float32(response[4:8])
        i_gain        = self.NanonisTCP.hex_to_float32(response[8:12])
        
        return [p_gain,time_constant,i_gain]