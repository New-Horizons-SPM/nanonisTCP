# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 18:33:28 2022

@author: Julian
"""

import numpy as np

class BiasSpectr:
    """
    Nanonis Bias Spectroscopy Module
    """
    def __init__(self,NanonisTCP):
        self.NanonisTCP = NanonisTCP
        
    def Open(self):
        """
        Opens the Bias Spectroscopy Module

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.Open', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def Start(self,get_data,save_base_name=""):
        """
        Starts a bias spectroscopy in the Bias Spectroscopy module.
        
        Before using this function, select the channels to record in the Bias
        Spectroscopy module.

        Parameters
        ----------
        get_data        : defines if the function returns the spectroscopy data
                          True: return data from this function
                          False: don't return data
        save_base_name  : Base name used by the saved files. Empty string 
                          keeps settings unchanged in nanonis
                    

        Returns
        -------
        if get_data  = False, this function returns None
        
        if get_data != False, this function returns:
            
        data_dict{
            '<channel_name>' : data for this channel
            }
        parameters  : List of fixed parameters and parameters (in that order).
                      To see the names of the returned parameters, use the 
                      BiasSpectr.PropsGet function

        """
        body_size = 4 + 4                                                       # 4 bytes for get_data (uint32) and 4 bytes for save_base_name_string_size (int)
        body_size = int(len(self.NanonisTCP.string_to_hex(save_base_name))/2)   # Variable size depending on the save_base_name string
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.Start', body_size=body_size)
        
        save_base_name_string_size = len(save_base_name)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(get_data,4)
        hex_rep += self.NanonisTCP.to_hex(save_base_name_string_size,4)
        if(save_base_name_string_size > 0):
            hex_rep += self.NanonisTCP.string_to_hex(save_base_name)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response
        response = self.NanonisTCP.receive_response()
        
        if(not get_data): return
        
        # channels_names_size = self.NanonisTCP.hex_to_int32(response[0:4])     # Useless
        number_of_channels  = self.NanonisTCP.hex_to_int32(response[4:8])
        
        idx = 8
        channel_names = []
        for i in range(number_of_channels):
            channel_name_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            channel_names.append(response[idx:idx + channel_name_size].decode())
            idx += channel_name_size
        
        data_rows = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        idx += 4
        data_cols = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        
        data_dict = {}
        for i in range(data_rows):
            data = []
            for j in range(data_cols):
                idx += 4
                data.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
            data_dict[channel_names[i]] = np.array(data)
        
        idx += 4
        parameters = []
        number_of_parameters = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        for i in range(number_of_parameters):
            idx += 4
            parameter = self.NanonisTCP.hex_to_float32(response[idx:idx+4])
            parameters.append(parameter)
        
        return [data_dict,parameters]
    
    def Stop(self):
        """
        Stops the current Bias Spectroscopy measurement.

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.Stop', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def StatusGet(self):
        """
        Returns the status of the Bias Spectroscopy measurement.
        
        Returns
        -------
        status : 0: Not running. 1: Running

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.StatusGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        status = self.NanonisTCP.hex_to_int32(response[0:4])
        
        return status
        
    # def ChsSet(self,channel_indexes)
        