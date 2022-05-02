# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 13:32:43 2022

@author: jced0001
"""

import numpy as np

class BiasSpectroscopy:
    """
    Nanonis Bias Spectroscopy Module
    """
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def Open(self):
        """
        Opens the Bias Spectroscopy module

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.Open', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def Start(self,get_data=True,save_base_name=""):
        """
        Starts a bias spectroscopy in the Bias Spectroscopy module

        Parameters
        ----------
        get_data       : defines if the function returns the spectroscopy data
                         True:  returns data
                         False: doesn't return data and the function returns 
                                without a response
        
        save_base_name : the basename used by the saved files.
                         "" (empty string): no change - leave setting as is
        Returns
        -------
        channels_names : the list of channels names
        data           : 2D data matrix where each row is the data for one 
                         channel
        parameters     : returns the list of fixed parameters and parameters (
                         in that order). To see the names of the returned 
                         parameters, use the BiasSpectr.PropsGet function

        """
        save_base_name_hex  = self.NanonisTCP.string_to_hex(save_base_name)
        save_base_name_size = int(len(save_base_name_hex)/2)
        body_size = 8 + save_base_name_size
        
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.Start', body_size=body_size,resp=get_data)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(get_data, 4)
        
        hex_rep += self.NanonisTCP.to_hex(save_base_name_size, 4)
        hex_rep += save_base_name_hex
        
        self.NanonisTCP.send_command(hex_rep)
        
        if(not get_data): return [0,0,0]
        
        # Receive Response
        response = self.NanonisTCP.receive_response()
        
        # channels_names_size = self.NanonisTCP.hex_to_int32(response[0:4])     # Not needed
        number_of_channels  = self.NanonisTCP.hex_to_int32(response[4:8])
        
        if(not number_of_channels): return [0,0,0]                              # Return if there are no channels selected (should always be at least one channel)
        
        idx = 8
        channels_names = []
        for i in range(number_of_channels):
            size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            
            idx += 4
            channels_names.append(response[idx:idx+size].decode())
            idx += size
        
        data_rows = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        
        idx += 4
        data_cols = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        
        data = np.empty((data_rows,data_cols))
        for i in range(data_rows):
            for j in range(data_cols):
                idx += 4
                data[i,j] = self.NanonisTCP.hex_to_float32(response[idx:idx+4])
        
        idx += 4
        number_of_parameters = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        
        parameters = []
        for i in range(number_of_parameters):
            idx += 4
            parameters.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
        
        return [channels_names,data,parameters]
    
    def Stop(self):
        """
        Stops the current Bias Spectroscopy measurement
        
        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.Stop', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)