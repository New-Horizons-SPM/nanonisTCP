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
        
        bias = self.NanonisTCP.hex_to_float32(response[0:4])
        return bias
    
    def RangeSet(self,bias_range_index):
        """
        Sets the range of the Bias voltage, if different ranges are available

        Parameters
        bias_range_index : is the index out of the list of ranges which can be 
                           retrieved by the function Bias.RangeGet

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Bias.RangeSet', body_size=2)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(bias_range_index,2)                   # uint16
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response (check errors)
        self.NanonisTCP.receive_response(0)
        
    def RangeGet(self):
        """
        Returns the selectable ranges of bias voltage and the index of the 
        selected one

        Returns
        bias_ranges      : returns an array of selectable bias ranges (if your
                           system supports it switching. see bias module doco)
        bias_range_index : is the index out of the list of bias ranges

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Bias.RangeGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response
        response = self.NanonisTCP.receive_response()                           # Not checking for errors because return arguments are variable size
        
        # bias_ranges_size = self.NanonisTCP.hex_to_int32(response[0:4])        # Not needed.
        
        number_of_ranges = self.NanonisTCP.hex_to_int32(response[4:8])
        bias_ranges      = []
        idx = 8
        for i in range(number_of_ranges):
            size = self.NanonisTCP.hex_to_uint32(response[idx:idx+4])
            
            idx += 4
            bias_ranges.append(response[idx:idx+size].decode())
            idx += size
            
        bias_range_index = self.NanonisTCP.hex_to_uint16(response[idx:idx+2])
        
        return [bias_ranges, bias_range_index]
    
    def CalibrSet(self,calibration,offset):
        """
        Set the calibration and offset of bias voltage

        Parameters
        ----------
        calibration : calibration
        offset      : offset

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Bias.CalibrSet', body_size=8)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(calibration)
        hex_rep += self.NanonisTCP.float32_to_hex(offset)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response (check errors)
        self.NanonisTCP.receive_response(0)
    
    def CalibrGet(self):
        """
        Gets the calibration and offset of bias voltage

        Returns
        -------
        calibration : calibration
        offset      : offset

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Bias.CalibrGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response
        response = self.NanonisTCP.receive_response(8)
        
        calibration = self.NanonisTCP.hex_to_float32(response[0:4])
        offset      = self.NanonisTCP.hex_to_float32(response[4:8])
        
        return [calibration,offset]
    
    def Pulse(self,bias_pulse_width,bias_value,z_hold=0,rel_abs=0,wait_until_done=False):
        """
        Generates one bias pulse

        Parameters
        ----------
        bias_pulse_width : is the pulse duration in seconds
        bias_value       : is the bias value applied during the pulse
        z_hold           : sets whether the controller is set to hold
                           (deactivated) during the pulse.
                           0: no change (leave setting as is in nanonis)
                           1: hold
                           2: don't hold
        rel_abs          : sets whether the bias value argument is an absolute
                           value or relative to the current bias
                           0: no change (leave setting as is in nanonis)
                           1: hold
                           2: absolute
        wait_until_done  : 0: don't wait
                           1: wait until function is done

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Bias.Pulse', body_size=16)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(wait_until_done,4)
        hex_rep += self.NanonisTCP.float32_to_hex(bias_pulse_width)
        hex_rep += self.NanonisTCP.float32_to_hex(bias_value)
        hex_rep += self.NanonisTCP.to_hex(z_hold,2)
        hex_rep += self.NanonisTCP.to_hex(rel_abs,2)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response (check errors)
        self.NanonisTCP.receive_response(0)