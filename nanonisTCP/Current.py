# -*- coding: utf-8 -*-
"""
Created on Sun May 29 09:02:02 2022

@author: Julian Ceddia
"""

class Current:
    """
    Nanonis Current Module
    """
    def __init__(self,NanonisTCP):
        self.NanonisTCP = NanonisTCP
        self.version = NanonisTCP.version
    
    def Get(self):
        """
        Returns the tunnelling current value

        Returns
        -------
        current : Current value (A)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Current.Get', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        current = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return current
    
    def Get100(self):
        """
        Returns the current value of the "Current 100" module

        Returns
        -------
        current100 : Current 100 value (A)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Current.100Get', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        current100 = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return current100
    
    def BEEMGet(self):
        """
        Returns the BEEM current value of the corresponding module in a BEEM
        system

        Returns
        -------
        currentBEEM : Current BEEM value (A)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Current.BEEMGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        currentBEEM = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return currentBEEM
    
    def GainSet(self,gain_index,filter_index=-1):
        """
        Sets the gain of the current amplifier

        Parameters
        ----------
        gain_index : The index out of the list of gains which can be retrieved
                     by the function Current.GainsGet
        filter_index : Nanonis version > 11798 only
                       The index out of the list of filters which can be retrieved by the function
                       Current.GainsGet. This is the list of filters available for the Basel PI SP 983c preamplifier. If the
                       preamplifier in use is not this one or we don’t want to change this parameter, -1 should be used.
        """
        if(self.version  < 11798): return self.GainSet_v0(gain_index)
        if(self.version >= 11798): return self.GainSet_v1(gain_index,filter_index)
        
    def GainSet_v0(self,gain_index):
        """
        Sets the gain of the current amplifier

        Parameters
        ----------
        gain_index : The index out of the list of gains which can be retrieved
                     by the function Current.GainsGet

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Current.GainSet', body_size=2)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(gain_index,2)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
           
    def GainSet_v1(self,gain_index, filter_index=-1):
        """
        Sets the gain of the current amplifier

        Parameters
        ----------
        gain_index : The index out of the list of gains which can be retrieved
                     by the function Current.GainsGet

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Current.GainSet', body_size=8)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(gain_index,4)
        hex_rep += self.NanonisTCP.to_hex(filter_index,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def GainsGet(self):
        """
        Returns the selectable gains of the current amplifier and the index of 
        the selected one

        Returns
        -------
        gains      : array of selectable gains
        gain_index : index of the selected gain in gains array

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Current.GainsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        # gains_size      = self.NanonisTCP.hex_to_int32(response[0:4])         # Not needed since
        number_of_gains = self.NanonisTCP.hex_to_int32(response[4:8])           # We know the number of gains
        
        idx   = 8
        gains = []
        for g in range(number_of_gains):
            size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])            # And the size of each next gain
            idx += 4
            gain = response[idx:idx+size].decode()
            idx += size
            gains.append(gain)
        
        gain_index = self.NanonisTCP.hex_to_uint16(response[idx:idx+2])
        
        return [gains,gain_index]
    
    def CalibrSet(self,calibration,offset):
        """
        Sets the calibration and offset of the selected gain in the current 
        module

        Parameters
        ----------
        calibration : calibration factor (A/V)
        offset      : offset (A)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Current.CalibrSet', body_size=16)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float64_to_hex(calibration)
        hex_rep += self.NanonisTCP.float64_to_hex(offset)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def CalibrGet(self):
        """
        Gets the calibration and offset of the selected gain in the current 
        module

        Returns
        -------
        callibtation : calibration (A/V)
        offset       : offset (A)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Current.CalibrGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(16)
        
        calibration = self.NanonisTCP.hex_to_float64(response[0:8])
        offset      = self.NanonisTCP.hex_to_float64(response[8:16])
        
        return [calibration,offset]