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
        self.version = NanonisTCP.version
        
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
        body_size += int(len(self.NanonisTCP.string_to_hex(save_base_name))/2)   # Variable size depending on the save_base_name string
        
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.Start', body_size=body_size)
        
        save_base_name_string_size = len(save_base_name)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(get_data,4)
        hex_rep += self.NanonisTCP.to_hex(save_base_name_string_size,4)
        if(save_base_name_string_size > 0):
            hex_rep += self.NanonisTCP.string_to_hex(save_base_name)
        
        self.NanonisTCP.send_command(hex_rep)
        
        if(not get_data == 1):
            response = self.NanonisTCP.receive_response(0)
            return
        
        # Receive Response
        response = self.NanonisTCP.receive_response()
        
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
        
        return {"data_dict"  : data_dict,
                "parameters" : parameters}
    
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
        
    def ChsSet(self,channel_indexes,mode="set"):
        """
        Sets/adds/removes the list of recorded channels in Bias Spectroscopy

        Parameters
        ----------
        channel_indexes : Nanonis v < R11798, use slot number:
                          channel indexes to set, add, or remove. The indexes 
                          are comprised between 0 and 23 for the 24 signals 
                          assigned in the Signals Manager. To get the signal 
                          name and its corresponding index in the list of 128 
                          available signals in the Nanonis Controller, use 
                          the Signals.InSlotsGet function

                          Nanonis v >= R11798, use RT Index:
                          indexes of recorded channels. The index is comprised between 0
                          and 127, and it corresponds to the full list of signals available in the system.
                          To get the signal name and its corresponding index in the list of the 128 available signals in the Nanonis
                          Controller, use the Signal.NamesGet function, or check the RT Idx value in the Signals Manager module.


        mode            : "set"    : channel_indexes will become the entire 
                                     list of selected channels
                          "add"    : channel_indexes will be added to the list 
                                     of selected channels
                          "remove" : remove channel_indexes from list of 
                                     selected channels

        """
        if(mode not in ["set","add","remove"]):
            raise Exception("Invalid mode for BiasSpectr.ChsSet. Must be one" +
                            "of 'set', 'add', 'remove'. Got " + str(mode))
        
        if(mode == "add"):
            buf_channel_indexes = self.ChsGet()
            for buf_index in buf_channel_indexes:
                if(buf_index not in channel_indexes):
                    channel_indexes.append(buf_index)
            
        if(mode == "remove"):
            buf_channel_indexes = self.ChsGet()
            for index in channel_indexes:
                if(index in buf_channel_indexes):
                    buf_channel_indexes.remove(index)
            channel_indexes = buf_channel_indexes
            
        number_of_channels = len(channel_indexes)
        body_size = 4 + number_of_channels*4                                    # 4 bytes for number_of_channels (int), plus 4 bytes for the integer array of channel_indexes
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.ChsSet', body_size=body_size)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(number_of_channels,4)
        for index in channel_indexes:
            hex_rep += self.NanonisTCP.to_hex(index,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def ChsGet(self):
        if(self.version  < 11798): return self.ChsGet_v0()
        if(self.version >= 11798): return self.ChsGet_v1()

    def ChsGet_v0(self):
        """
        Returns the list of recorded channels in Bias Spectroscopy

        Returns
        -------
        channel_indexes : The indexes of recorded channels. The indexes are 
                          comprised between 0 and 23 for the 24 signals 
                          assigned in the signals manager.
                          To get the signal name and its corresponding index in
                          the list of 128 available signals in the Nanonis
                          Controller, use the Signals.InSlotsGet function

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.ChsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        number_of_channels = self.NanonisTCP.hex_to_int32(response[0:4])
        
        idx = 4
        channel_indexes = []
        for i in range(number_of_channels):
            channel_index = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            channel_indexes.append(channel_index)
            idx += 4
        
        return channel_indexes
    
    def ChsGet_v1(self):
        """
        Returns the list of recorded channels in Bias Spectroscopy

        Returns
        -------
        channel_indexes :  The index is comprised between 0
                           and 127, and it corresponds to the 
                           full list of signals available in 
                           the system. To get the signal name
                           and its corresponding index in the
                           list of the 128 available signals
                           in the Nanonis Controller, use the 
                           Signal.NamesGet function, or check 
                           the RT Idx value in the Signals 
                           Manager module.
        channel_names   :  Returns the names of the acquired
                           channels in the sweep

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.ChsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        number_of_channels = self.NanonisTCP.hex_to_int32(response[0:4])
        
        idx = 4
        channel_indexes = []
        for i in range(number_of_channels):
            channel_index = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            channel_indexes.append(channel_index)
            idx += 4
        
        # channels_size = self.NanonisTCP.hex_to_int32(response[12:16])         # Useless
        idx += 4
        channels_names = []
        num_channels = len(channel_indexes)
        for channel in range(num_channels):
            channel_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            channels_names.append(response[idx:idx+channel_size].decode())
            idx += channel_size

        return channel_indexes, channels_names
        
    def PropsSet(self,save_all=0,num_sweeps=0,back_sweep=0,num_points=0,z_offset=0,autosave=0,save_dialog=0):
        """
        Configures the Bias Spectroscopy parameters

        Returns
        -------
        save_all : 0 : no change
                   1 : data from individual sweeps is saved, along with 
                       averaged data.
                   2 : Individual sweeps are not saved, only the average of 
                       all of them is saved. This parameter only makes sense 
                       when multiple sweeps are configured.
        num_sweeps : Number of sweeps to measure and average. 0 means no change
        back_sweep : Selects whether a backward sweep is acquired in addition 
                     to the forward sweep (which is always acquired)
                     0 : No change
                     1 : Don't acquire a backward sweep.
                     2 : Acquire a backward sweep (in addition to the forward)
        num_points : Defines the number of points to acquire over the sweep
                     range. 0 means no change
        z_offset   : Defines which distance (m) to move the tip before starting
                     the measurement. Positive value means retracting,
                     negative value means approaching.
        autosave   : Selects whether to automatically save the data to ASCII 
                     file once the sweep is done.
                     0 : No change
                     1 : Autosave data after acquisition
                     2 : Don't autosave after acquisition
        save_dialog : Selects whether to show the save dialog box once the 
                      sweep is done.
                      0 : No change
                      1 : Show the save dialog box after sweep
                      2 : Don't show the save dialog box after sweep

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.PropsSet', body_size=20)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(save_all,2)
        hex_rep += self.NanonisTCP.to_hex(num_sweeps,4)
        hex_rep += self.NanonisTCP.to_hex(back_sweep,2)
        hex_rep += self.NanonisTCP.to_hex(num_points,4)
        hex_rep += self.NanonisTCP.float32_to_hex(z_offset)
        hex_rep += self.NanonisTCP.to_hex(autosave,2)
        hex_rep += self.NanonisTCP.to_hex(save_dialog,2)
        
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def PropsGet(self):
        if(self.version  < 11798): return self.PropsGet_v0()
        if(self.version >= 11798): return self.PropsGet_v1()
        
    def PropsGet_v0(self):
        """
        Returns the Bias Spectroscopy parameters

        Returns
        -------
        save_all : 1 : data from individual sweeps is saved, along with 
                       averaged data.
                   0 : Individual sweeps are not saved, only the average of 
                       all of them is saved. This parameter only makes sense 
                       when multiple sweeps are configured.
        num_sweeps : Number of sweeps to measure and average. 0 means no change
        back_sweep : Selects whether a backward sweep is acquired in addition 
                     to the forward sweep (which is always acquired)
                     0 : Don't acquire a backward sweep.
                     1 : Acquire a backward sweep (in addition to the forward)
        num_points : Defines the number of points to acquire over the sweep
                     range. 0 means no change
        channels   : Returns the names of the acquired channels in the sweep.
        parameters : Returns the parameters of the sweep
        fixed_parameters : Returns the fixed parameters of the sweep
        
        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.PropsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        save_all   = self.NanonisTCP.hex_to_int16(response[0:2])
        num_sweeps = self.NanonisTCP.hex_to_int32(response[2:6])
        back_sweep = self.NanonisTCP.hex_to_int16(response[6:8])
        num_points = self.NanonisTCP.hex_to_int32(response[8:12])
        
        # channels_size = self.NanonisTCP.hex_to_int32(response[12:16])         # Useless
        idx = 20
        channels = []
        num_channels = self.NanonisTCP.hex_to_int32(response[16:20])
        for channel in range(num_channels):
            channel_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            channels.append(response[idx:idx+channel_size].decode())
            idx += channel_size
            
        # parameters_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])   # Useless
        
        idx += 4
        parameters = []
        num_parameters  = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        idx += 4
        for parameter in range(num_parameters):
            parameter_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            parameters.append(response[idx:idx+parameter_size].decode())
            idx += parameter_size
            
        # fixed_parameters_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4]) # Useless
        idx += 4
        fixed_parameters = []
        num_fixed_parameters  = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        idx += 4
        for fixed_parameter in range(num_fixed_parameters):
            fixed_parameter_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            fixed_parameters.append(response[idx:idx+fixed_parameter_size].decode())
            idx += fixed_parameter_size
        
        return {"save_all"    : save_all,
                "num_sweeps"  : num_sweeps,
                "back_sweep"  : back_sweep,
                "num_points"  : num_points,
                "channels"    : channels,
                "parameters"  : parameters,
                "fixed_parameters" : fixed_parameters}
    
    def PropsGet_v1(self):
        """
        Returns the Bias Spectroscopy parameters

        Returns
        -------
        save_all : 1 : data from individual sweeps is saved, along with 
                       averaged data.
                   0 : Individual sweeps are not saved, only the average of 
                       all of them is saved. This parameter only makes sense 
                       when multiple sweeps are configured.
        num_sweeps : Number of sweeps to measure and average. 0 means no change
        back_sweep : Selects whether a backward sweep is acquired in addition 
                     to the forward sweep (which is always acquired)
                     0 : Don't acquire a backward sweep.
                     1 : Acquire a backward sweep (in addition to the forward)
        num_points : Defines the number of points to acquire over the sweep
                     range. 0 means no change
        parameters : Returns the parameters of the sweep
        fixed_parameters : Returns the fixed parameters of the sweep
        autosave    : Selects whether to automatically save the data to ASCII
                      file once the sweep is done.
                      0 : Autosave off
                      1 : Autosave on
        save_dialog : Selects whether to show the save dialog box once the 
                      sweep is done
                      0 : Don't show
                      1 : Show
        
        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.PropsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        save_all   = self.NanonisTCP.hex_to_int16(response[0:2])
        num_sweeps = self.NanonisTCP.hex_to_int32(response[2:6])
        back_sweep = self.NanonisTCP.hex_to_int16(response[6:8])
        num_points = self.NanonisTCP.hex_to_int32(response[8:12])
        idx = 12

        # parameters_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])   # Useless

        idx += 4
        parameters = []
        num_parameters  = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        idx += 4
        for parameter in range(num_parameters):
            parameter_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            parameters.append(response[idx:idx+parameter_size].decode())
            idx += parameter_size
            
        # fixed_parameters_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4]) # Useless
        idx += 4
        fixed_parameters = []
        num_fixed_parameters  = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        idx += 4
        for fixed_parameter in range(num_fixed_parameters):
            fixed_parameter_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            fixed_parameters.append(response[idx:idx+fixed_parameter_size].decode())
            idx += fixed_parameter_size
        
        autosave    = self.NanonisTCP.hex_to_int16(response[idx:idx+4]); idx += 4
        save_dialog = self.NanonisTCP.hex_to_int16(response[idx:idx+4]); idx += 4

        return {"save_all"    : save_all,
                "num_sweeps"  : num_sweeps,
                "back_sweep"  : back_sweep,
                "num_points"  : num_points,
                "parameters"  : parameters,
                "fixed_parameters" : fixed_parameters,
                "autosave"    : autosave,
                "save_dialog" : save_dialog}
    
    def AdvPropsSet(self,reset_bias=0,z_controller_hold=0,record_final_z=0,lockin_run=0):
        """
        Sets parameters from the advanced configuration section of the bias 
        spectroscopy module.

        Parameters
        ----------
        reset_bias          : Sets whether the Bias voltage returns to the 
                              initial value at the end of the spectroscopy 
                              measurement.
                              0: no change
                              1: on
                              2: off
        z_controller_hold   : Sets the Z-Controller on hold during the sweeo.
                              0: no change
                              1: on
                              2: off
        record_final_z      : Records the Z position during the Z averaging 
                              time at the end of the sweep.
                              0: no change
                              1: on
                              2: off
        lockin_run          : Sets the lock-in to run during the measurement
                              0: no change
                              1: on
                              2: off

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.AdvPropsSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(reset_bias,2)
        hex_rep += self.NanonisTCP.to_hex(z_controller_hold,2)
        hex_rep += self.NanonisTCP.to_hex(record_final_z,2)
        hex_rep += self.NanonisTCP.to_hex(lockin_run,2)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def AdvPropsGet(self):
        """
        Returns parameters from the advanced configuration section of the bias 
        spectroscopy module.

        Parameters
        ----------
        reset_bias          : Sets whether the Bias voltage returns to the 
                              initial value at the end of the spectroscopy 
                              measurement.
                              1: on
                              0: off
        z_controller_hold   : Sets the Z-Controller on hold during the sweeo.
                              1: on
                              0: off
        record_final_z      : Records the Z position during the Z averaging 
                              time at the end of the sweep.
                              1: on
                              0: off
        lockin_run          : Sets the lock-in to run during the measurement
                              1: on
                              0: off

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.AdvPropsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        reset_bias          = self.NanonisTCP.hex_to_int16(response[0:2])
        z_controller_hold   = self.NanonisTCP.hex_to_int16(response[2:4])
        record_final_z      = self.NanonisTCP.hex_to_int16(response[4:6])
        lockin_run          = self.NanonisTCP.hex_to_int16(response[6:8])
        
        return {"reset_bias"        : reset_bias,
                "z_controller_hold" : z_controller_hold,
                "record_final_z"    : record_final_z,
                "lockin_run"        : lockin_run}
    
    def LimitsSet(self,start_value,end_value):
        """
        Sets the Bias spectroscopy limits.

        Parameters
        ----------
        start_value : is the starting value of the sweep
        end_value   : is the ending value of the sweep
        
        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.LimitsSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.float32_to_hex(start_value)
        hex_rep += self.NanonisTCP.float32_to_hex(end_value)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def LimitsGet(self):
        """
        Returns the bias spectroscopy limits

        Returns
        -------
        start_value : is the starting value of the sweep
        end_value   : is the ending value of the sweep

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.LimitsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        start_value = self.NanonisTCP.hex_to_float32(response[0:4])
        end_value   = self.NanonisTCP.hex_to_float32(response[4:8])
        
        return {"start_value" : start_value,
                "end_value"   : end_value}
        
    def TimingSet(self,z_averaging_time,z_offset,initial_settling_time,maximum_slew_rate,settling_time,integration_time,end_settling_time,z_control_time):
        """
        Configures the bias spec timing parameters

        Parameters
        ----------
        z_averaging_time :      
        z_offset :              
        initial_settling_time : 
        maximum_slew_rate :     
        settling_time :         
        integration_time :      
        end_settling_time :     
        z_control_time :        

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.TimingSet', body_size=32)
        
        ## arguments
        hex_rep += self.NanonisTCP.float32_to_hex(z_averaging_time)
        hex_rep += self.NanonisTCP.float32_to_hex(z_offset)
        hex_rep += self.NanonisTCP.float32_to_hex(initial_settling_time)
        hex_rep += self.NanonisTCP.float32_to_hex(maximum_slew_rate)
        hex_rep += self.NanonisTCP.float32_to_hex(settling_time)
        hex_rep += self.NanonisTCP.float32_to_hex(integration_time)
        hex_rep += self.NanonisTCP.float32_to_hex(end_settling_time)
        hex_rep += self.NanonisTCP.float32_to_hex(z_control_time)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def TimingGet(self):
        """
        Returns the bias spec timing params

        Returns
        -------
        z_averaging_time :      
        z_offset :              
        initial_settling_time : 
        maximum_slew_rate :     
        settling_time :         
        integration_time :      
        end_settling_time :     
        z_control_time :        

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.TimingGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        z_averaging_time        = self.NanonisTCP.hex_to_float32(response[0:4])
        z_offset                = self.NanonisTCP.hex_to_float32(response[4:8])
        initial_settling_time   = self.NanonisTCP.hex_to_float32(response[8:12])
        maximum_slew_rate       = self.NanonisTCP.hex_to_float32(response[12:16])
        settling_time           = self.NanonisTCP.hex_to_float32(response[16:20])
        integration_time        = self.NanonisTCP.hex_to_float32(response[20:24])
        end_settling_time       = self.NanonisTCP.hex_to_float32(response[24:28])
        z_control_time          = self.NanonisTCP.hex_to_float32(response[28:32])
        
        return {"z_averaging_time"      : z_averaging_time,
                "z_offset"              : z_offset,
                "initial_settling_time" : initial_settling_time,
                "maximum_slew_rate"     : maximum_slew_rate,
                "settling_time"         : settling_time,
                "integration_time"      : integration_time,
                "end_settling_time"     : end_settling_time,
                "z_control_time"        : z_control_time}
    
    # def TTLSyncSet(self)
    # def TTLSyncGet(self)
    
    def AltZCtrlSet(self,alternate_setpoint_onoff,setpoint,settling_time):
        """
        Sets the configuration of the alternate z-controller setpoint in the
        advanced section of the bias spec module.
        
        When switched on, the z-controller setpoint is set to <setpoint> 
        right after starting the measuremnt. After changing the setpoint, the 
        settling time (s) will be waited for the z-controller to adjust to the 
        modified setpoint.
        
        Then the z averaging will start. The original z-controller setpoint is 
        restored at the end of the measurement, before restoring the
        z-controller state.

        Parameters
        ----------
        alternate_setpoint_onoff :  Turn the alternate z-controller setpoint on
                                    0: no change
                                    1: on
                                    2: off
        setpoint :                  setpoint for spectroscopy (A)
        settling_time :             Settling time (s)

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.AltZCtrlSet', body_size=10)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(alternate_setpoint_onoff,2)
        hex_rep += self.NanonisTCP.float32_to_hex(setpoint)
        hex_rep += self.NanonisTCP.float32_to_hex(settling_time)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def AltZCtrlGet(self):
        """
        Returns the configuration of the alternate z-controller setpoint in the
        advanced section of the bias spec module

        Returns
        -------
        alternate_setpoint_onoff :  Turn the alternate z-controller setpoint on
                                    0: off
                                    1: on
        setpoint :                  setpoint for spectroscopy (A)
        settling_time :             Settling time (s)

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.AltZCtrlGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        alternate_setpoint_onoff = self.NanonisTCP.hex_to_uint16(response[0:2])
        setpoint                 = self.NanonisTCP.hex_to_float32(response[2:6])
        settling_time            = self.NanonisTCP.hex_to_float32(response[6:10])
        
        return {"alternate_setpoint_onoff"  : alternate_setpoint_onoff,
                "setpoint"                  : setpoint,
                "settling_time"             : settling_time}
    
    def MLSLockinPerSegSet(self,lockin_per_segment):
        """
        Sets the Lock-In Per Segment flag in the multi line segment editor
        
        When selected, the Lock-In can be defined per segment in the Multi line 
        segment editor. Otherwise, the Lock-In is set globally according to the 
        flag in the Advanced section of Bias spectroscopy

        Parameters
        ----------
        lockin_per_segment : 0: off; 1: on

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.MLSLockinPerSegSet', body_size=4)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(lockin_per_segment,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def MLSLockinPerSegGet(self):
        """
        Returns the Lock-In per Segment flag in the Multi line segment editor.
        When selected, the Lock-In can be defined per segment in the Multi line
        segment editor. Otherwise, the Lock-In is set globally according to the 
        flag in the Advanced section of Bias spectroscopy

        Returns
        -------
        lockin_per_segment : 0: off; 1: on

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.MLSLockinPerSegGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        lockin_per_segment = self.NanonisTCP.hex_to_uint32(response[0:4])
        
        return lockin_per_segment
    
    def MLSModeSet(self,sweep_mode):
        """
        Sets the Bias Spectroscopy sweep mode.

        Parameters
        ----------
        sweep_mode : "linear" for linear or "MLS" for MultiSegment mode

        """
        if(sweep_mode.lower() == "linear"): sweep_mode = "Linear"
        if(sweep_mode.lower() == "mls"):    sweep_mode = "MLS"
        sweep_mode_size = len(sweep_mode)
        
        body_size = 4 + int(len(self.NanonisTCP.string_to_hex(sweep_mode))/2)
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.MLSModeSet', body_size=body_size)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(sweep_mode_size,4)
        hex_rep += self.NanonisTCP.string_to_hex(sweep_mode)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def MLSModeGet(self):
        """
        Returns the Bias Spectroscopy sweep mode.

        Returns
        -------
        sweep_mode : "linear" for linear or "MLS" for MultiSegment mode

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.MLSModeGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        sweep_mode = response[4:].decode()
        
        return sweep_mode
    
    def MLSValsSet(self,bias_start,bias_end,initial_settling_time,settling_time,integration_time,steps,lockin_run):
        """
        Sets the bias spectroscopy multiple line segment configuration for 
        Multi Line Segment mode. Up to 16 distinct line segments may be 
        defined. Any segments beyond the maximum allowed amount will be ignored
        
        Parameters (all type list)
        ----------
        bias_start              : list of bias start values for each segment (V)
        bias_end                : list of bias end values for each segment (V)
        initial_settling_time   : time to wait at begining of each segment
                                  before Lock-In setting is applied (s)
        settling_time           : time to wait before measuring each data point
                                  for each segment (s)
        integration_time        : integration time for each data point for 
                                  each segment (s)
        steps                   : number of steps to measure in each segment
        lockin_run              : indicates if the Lock-In will run during the 
                                  segment. This is true only if the global 
                                  Lock-In per Segment flag is enabled.
                                  Otherwise, the Lock-In is set globally 
                                  according to the flag in the Advanced section 
                                  of Bias spectroscopy
        """
        if(not type(bias_start) is list): bias_start = [bias_start]
        if(not type(bias_end) is list): bias_end = [bias_end]
        if(not type(initial_settling_time) is list): initial_settling_time = [initial_settling_time]
        if(not type(settling_time) is list): settling_time = [settling_time]
        if(not type(integration_time) is list): integration_time = [integration_time]
        if(not type(steps) is list): steps = [steps]
        if(not type(lockin_run) is list): lockin_run = [lockin_run]
        
        num_segments = len(bias_start)
        
        body_size = 4 + num_segments*(4 + 4 + 4 + 4 + 4 + 4 + 4)
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.MLSValsSet', body_size=body_size)
        
        hex_rep += self.NanonisTCP.to_hex(num_segments,4)
        
        for p in bias_start:
            hex_rep += self.NanonisTCP.float32_to_hex(p)
            
        for p in bias_end:
            hex_rep += self.NanonisTCP.float32_to_hex(p)
            
        for p in initial_settling_time:
            hex_rep += self.NanonisTCP.float32_to_hex(p)
            
        for p in settling_time:
            hex_rep += self.NanonisTCP.float32_to_hex(p)
            
        for p in integration_time:
            hex_rep += self.NanonisTCP.float32_to_hex(p)
            
        for p in steps:
            hex_rep += self.NanonisTCP.to_hex(p,4)
            
        for p in lockin_run:
            hex_rep += self.NanonisTCP.to_hex(p,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def MLSValsGet(self):
        """
        Returns the bias spectroscopy multiple line segment configuration for 
        Multi Line Segment mode. Up to 16 distinct line segments may be defined.

        Returns
        -------
        bias_start              : list of bias start values for each segment (V)
        bias_end                : list of bias end values for each segment (V)
        initial_settling_time   : time to wait at begining of each segment
                                  before Lock-In setting is applied (s)
        settling_time           : time to wait before measuring each data point
                                  for each segment (s)
        integration_time        : integration time for each data point for 
                                  each segment (s)
        steps                   : number of steps to measure in each segment
        lockin_run              : indicates if the Lock-In will run during the 
                                  segment. This is true only if the global 
                                  Lock-In per Segment flag is enabled.
                                  Otherwise, the Lock-In is set globally 
                                  according to the flag in the Advanced section 
                                  of Bias spectroscopy

        """
        hex_rep = self.NanonisTCP.make_header('BiasSpectr.MLSValsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        num_segments = self.NanonisTCP.hex_to_int32(response[0:4])
        
        idx = 4
        bias_start = []
        for p in range(num_segments):
            bias_start.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
            idx += 4
            
        bias_end = []
        for p in range(num_segments):
            bias_end.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
            idx += 4
            
        initial_settling_time = []
        for p in range(num_segments):
            initial_settling_time.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
            idx += 4
            
        settling_time = []
        for p in range(num_segments):
            settling_time.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
            idx += 4
        
        integration_time = []
        for p in range(num_segments):
            integration_time.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
            idx += 4
            
        steps = []
        for p in range(num_segments):
            steps.append(self.NanonisTCP.hex_to_int32(response[idx:idx+4]))
            idx += 4
            
        lockin_run = []
        for p in range(num_segments):
            lockin_run.append(self.NanonisTCP.hex_to_uint32(response[idx:idx+4]))
            idx += 4
        
        retDict = {"bias_start"             : bias_start,
                   "bias_end"               : bias_end,
                   "initial_settling_time"  : initial_settling_time,
                   "settling_time"          : settling_time,
                   "integration_time"       : integration_time,
                   "steps"                  : steps,
                   "lockin_run"             : lockin_run}
        
        return retDict