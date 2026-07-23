# -*- coding: utf-8 -*-
"""
Created on Mon May 25 2026

@author: Ben
Generated from Nanonis TCP Protocol (TCPProtocol_SPM_25-12-10)
"""

import numpy as np

class ZSpectr:
    """
    Nanonis Z Spectroscopy Module
    """
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
        self.version = NanonisTCP.version

    def Open(self):
        """
        Opens the Z Spectroscopy module.
        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.Open', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def Start(self, get_data, save_base_name=""):
        """
        Starts a Z spectroscopy in the Z Spectroscopy module.

        Before using this function, select the channels to record in the Z
        Spectroscopy module.

        Parameters
        ----------
        get_data        : defines if the function returns the spectroscopy data
                          True: return data from this function
                          False: don't return data
        save_base_name  : Base name used by the saved files. Empty string
                          keeps settings unchanged in Nanonis

        Returns
        -------
        if get_data = False, this function returns None

        if get_data != False, this function returns:

        data_dict{
            '<channel_name>' : data for this channel
            }
        parameters  : List of fixed parameters and parameters (in that order).
                      To see the names of the returned parameters, use the
                      ZSpectr.PropsGet function

        """
        body_size = 4 + 4                                                       # 4 bytes for get_data (uint32) and 4 bytes for save_base_name_string_size (int)
        body_size += int(len(self.NanonisTCP.string_to_hex(save_base_name))/2)  # Variable size depending on the save_base_name string

        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZSpectr.Start', body_size=body_size)

        save_base_name_string_size = len(save_base_name)

        ## arguments
        hex_rep += self.NanonisTCP.to_hex(get_data, 4)
        hex_rep += self.NanonisTCP.to_hex(save_base_name_string_size, 4)
        if save_base_name_string_size > 0:
            hex_rep += self.NanonisTCP.string_to_hex(save_base_name)

        self.NanonisTCP.send_command(hex_rep)

        if not get_data == 1:
            self.NanonisTCP.receive_response(0)
            return

        # Receive Response
        response = self.NanonisTCP.receive_response()

        # channels_names_size = self.NanonisTCP.hex_to_int32(response[0:4])     # Useless
        number_of_channels = self.NanonisTCP.hex_to_int32(response[4:8])

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
        Stops the current Z Spectroscopy measurement.
        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.Stop', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def StatusGet(self):
        """
        Returns the status of the Z Spectroscopy measurement.

        Returns
        -------
        status : 0: Not running. 1: Running

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.StatusGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response(4)

        status = self.NanonisTCP.hex_to_uint32(response[0:4])

        return status

    def ChsSet(self, channel_indexes, mode="set"):
        """
        Sets the list of recorded channels in Z Spectroscopy.

        Parameters
        ----------
        channel_indexes : indexes of recorded channels. The index is comprised
                          between 0 and 127, and it corresponds to the full
                          list of signals available in the system.
                          To get the signal name and its corresponding index in
                          the list of the 128 available signals in the Nanonis
                          Controller, use the Signal.NamesGet function, or
                          check the RT Idx value in the Signals Manager module.

        mode            : "set"    : channel_indexes will become the entire
                                     list of selected channels
                          "add"    : channel_indexes will be added to the list
                                     of selected channels
                          "remove" : remove channel_indexes from list of
                                     selected channels

        """
        if mode not in ["set", "add", "remove"]:
            raise Exception("Invalid mode for ZSpectr.ChsSet. Must be one of "
                            "'set', 'add', 'remove'. Got " + str(mode))

        if mode == "add":
            buf_channel_indexes, _ = self.ChsGet()
            for buf_index in buf_channel_indexes:
                if buf_index not in channel_indexes:
                    channel_indexes.append(buf_index)

        if mode == "remove":
            buf_channel_indexes, _ = self.ChsGet()
            for index in channel_indexes:
                if index in buf_channel_indexes:
                    buf_channel_indexes.remove(index)
            channel_indexes = buf_channel_indexes

        number_of_channels = len(channel_indexes)
        body_size = 4 + number_of_channels * 4                                  # 4 bytes for number_of_channels (int), plus 4 bytes per channel index
        hex_rep = self.NanonisTCP.make_header('ZSpectr.ChsSet', body_size=body_size)

        ## arguments
        hex_rep += self.NanonisTCP.to_hex(number_of_channels, 4)
        for index in channel_indexes:
            hex_rep += self.NanonisTCP.to_hex(index, 4)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def ChsGet(self):
        """
        Returns the list of recorded channels in Z Spectroscopy.

        Returns
        -------
        channel_indexes : The indexes of recorded channels. The index is
                          comprised between 0 and 127, and it corresponds to
                          the full list of signals available in the system.
                          To get the signal name and its corresponding index in
                          the list of the 128 available signals in the Nanonis
                          Controller, use the Signal.NamesGet function, or
                          check the RT Idx value in the Signals Manager module.
        channel_names   : Returns the names of the acquired channels in the
                          sweep (averages and individual sweeps in case the
                          save All flag is checked).

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.ChsGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response()

        number_of_channels = self.NanonisTCP.hex_to_int32(response[0:4])

        idx = 4
        channel_indexes = []
        for i in range(number_of_channels):
            channel_index = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            channel_indexes.append(channel_index)
            idx += 4

        # channels_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])     # Useless
        idx += 4
        num_channel_names = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        idx += 4
        channel_names = []
        for i in range(num_channel_names):
            channel_name_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            channel_names.append(response[idx:idx+channel_name_size].decode())
            idx += channel_name_size

        return channel_indexes, channel_names

    def PropsSet(self, back_sweep=0, num_points=0, num_sweeps=0, autosave=0, save_dialog=0, save_all=0):
        """
        Configures the Z Spectroscopy parameters.

        Parameters
        ----------
        back_sweep  : Selects whether a backward sweep is acquired in addition
                      to the forward sweep (which is always acquired).
                      0: No change
                      1: Acquire a backward sweep
                      2: Don't acquire a backward sweep
        num_points  : Defines the number of points to acquire over the sweep
                      range. 0 means no change.
        num_sweeps  : Number of sweeps to measure and average. 0 means no change.
        autosave    : Selects whether to automatically save the data to ASCII
                      file once the sweep is done.
                      0: No change
                      1: Autosave on
                      2: Autosave off
        save_dialog : Selects whether to show the save dialog box once the
                      sweep is done.
                      0: No change
                      1: Show the save dialog box
                      2: Don't show the save dialog box
        save_all    : 0: No change
                      1: Data from individual sweeps is saved along with
                         averaged data
                      2: Individual sweeps are not saved, only the average

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.PropsSet', body_size=14)

        ## arguments
        hex_rep += self.NanonisTCP.to_hex(back_sweep, 2)
        hex_rep += self.NanonisTCP.to_hex(num_points, 4)
        hex_rep += self.NanonisTCP.to_hex(num_sweeps, 2)
        hex_rep += self.NanonisTCP.to_hex(autosave, 2)
        hex_rep += self.NanonisTCP.to_hex(save_dialog, 2)
        hex_rep += self.NanonisTCP.to_hex(save_all, 2)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def PropsGet(self):
        """
        Returns the Z Spectroscopy parameters.

        Returns
        -------
        back_sweep       : 1: Backward sweep is performed (forward always measured)
                           0: No backward sweep
        num_points       : Number of points to acquire over the sweep range
        parameters       : Returns the parameters of the sweep
        fixed_parameters : Returns the fixed parameters of the sweep
        num_sweeps       : Number of sweeps to measure and average
        autosave         : 1: Autosave on; 0: Autosave off
        save_dialog      : 1: Show save dialog; 0: Don't show
        save_all         : 1: Individual sweeps saved along with average
                           0: Only average saved

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.PropsGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response()

        back_sweep = self.NanonisTCP.hex_to_uint16(response[0:2])
        num_points = self.NanonisTCP.hex_to_int32(response[2:6])

        idx = 6
        # parameters_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])   # Useless
        idx += 4
        parameters = []
        num_parameters = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        idx += 4
        for i in range(num_parameters):
            parameter_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            parameters.append(response[idx:idx+parameter_size].decode())
            idx += parameter_size

        # fixed_parameters_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4]) # Useless
        idx += 4
        fixed_parameters = []
        num_fixed_parameters = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        idx += 4
        for i in range(num_fixed_parameters):
            fixed_parameter_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            fixed_parameters.append(response[idx:idx+fixed_parameter_size].decode())
            idx += fixed_parameter_size

        num_sweeps  = self.NanonisTCP.hex_to_uint16(response[idx:idx+2]); idx += 2
        autosave    = self.NanonisTCP.hex_to_uint16(response[idx:idx+2]); idx += 2
        save_dialog = self.NanonisTCP.hex_to_uint16(response[idx:idx+2]); idx += 2
        save_all    = self.NanonisTCP.hex_to_uint16(response[idx:idx+2]); idx += 2

        return {"back_sweep"       : back_sweep,
                "num_points"       : num_points,
                "parameters"       : parameters,
                "fixed_parameters" : fixed_parameters,
                "num_sweeps"       : num_sweeps,
                "autosave"         : autosave,
                "save_dialog"      : save_dialog,
                "save_all"         : save_all}

    def AdvPropsSet(self, time_bw_sweep=0.0, record_final_z=0, lockin_run=0, reset_z=0):
        """
        Sets parameters from the Advanced configuration section of the Z
        spectroscopy module.

        Parameters
        ----------
        time_bw_sweep   : Time between forward and backward sweep (s) (float32)
        record_final_z  : If on, the final Z position is averaged during Z
                          averaging time after Z control time at the end of the
                          sweep.
                          0: No change; 1: On; 2: Off
        lockin_run      : Sets the Lock-In to run during the measurement.
                          0: No change; 1: On; 2: Off
        reset_z         : If on, the Z position is set back to the initial
                          value at the end of the sweep.
                          0: No change; 1: On; 2: Off

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.AdvPropsSet', body_size=12)

        ## arguments
        hex_rep += self.NanonisTCP.float32_to_hex(time_bw_sweep)
        hex_rep += self.NanonisTCP.to_hex(record_final_z, 2)
        hex_rep += self.NanonisTCP.to_hex(lockin_run, 2)
        hex_rep += self.NanonisTCP.to_hex(reset_z, 2)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def AdvPropsGet(self):
        """
        Returns parameters from the Advanced configuration section of the Z
        spectroscopy module.

        Returns
        -------
        time_bw_sweep   : Time between forward and backward sweep (s) (float32)
        record_final_z  : 0: Off; 1: On
        lockin_run      : 0: Off; 1: On
        reset_z         : 0: Off; 1: On

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.AdvPropsGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response()

        time_bw_sweep  = self.NanonisTCP.hex_to_float32(response[0:4])
        record_final_z = self.NanonisTCP.hex_to_uint16(response[4:6])
        lockin_run     = self.NanonisTCP.hex_to_uint16(response[6:8])
        reset_z        = self.NanonisTCP.hex_to_uint16(response[8:10])

        return {"time_bw_sweep"  : time_bw_sweep,
                "record_final_z" : record_final_z,
                "lockin_run"     : lockin_run,
                "reset_z"        : reset_z}

    def RangeSet(self, z_offset, z_sweep_distance):
        """
        Sets the Z-spectroscopy range settings.

        Parameters
        ----------
        z_offset        : Offset to apply before starting the sweep (m)
        z_sweep_distance: Sweep span (m)

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.RangeSet', body_size=8)

        ## arguments
        hex_rep += self.NanonisTCP.float32_to_hex(z_offset)
        hex_rep += self.NanonisTCP.float32_to_hex(z_sweep_distance)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def RangeGet(self):
        """
        Returns the Z-spectroscopy range settings.

        Returns
        -------
        z_offset        : Offset to apply before starting the sweep (m)
        z_sweep_distance: Sweep span (m)

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.RangeGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response()

        z_offset         = self.NanonisTCP.hex_to_float32(response[0:4])
        z_sweep_distance = self.NanonisTCP.hex_to_float32(response[4:8])

        return {"z_offset"         : z_offset,
                "z_sweep_distance" : z_sweep_distance}

    def TimingSet(self, z_averaging_time, initial_settling_time, maximum_slew_rate,
                  settling_time, integration_time, end_settling_time, z_control_time):
        """
        Configures the Z spectroscopy timing parameters.

        Parameters
        ----------
        z_averaging_time        : Z averaging time (s)
        initial_settling_time   : Initial settling time (s)
        maximum_slew_rate       : Maximum slew rate (V/s)
        settling_time           : Settling time (s)
        integration_time        : Integration time (s)
        end_settling_time       : End settling time (s)
        z_control_time          : Z control time (s)

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.TimingSet', body_size=28)

        ## arguments
        hex_rep += self.NanonisTCP.float32_to_hex(z_averaging_time)
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
        Returns the Z spectroscopy timing parameters.

        Returns
        -------
        z_averaging_time        : Z averaging time (s)
        initial_settling_time   : Initial settling time (s)
        maximum_slew_rate       : Maximum slew rate (V/s)
        settling_time           : Settling time (s)
        integration_time        : Integration time (s)
        end_settling_time       : End settling time (s)
        z_control_time          : Z control time (s)

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.TimingGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response()

        z_averaging_time      = self.NanonisTCP.hex_to_float32(response[0:4])
        initial_settling_time = self.NanonisTCP.hex_to_float32(response[4:8])
        maximum_slew_rate     = self.NanonisTCP.hex_to_float32(response[8:12])
        settling_time         = self.NanonisTCP.hex_to_float32(response[12:16])
        integration_time      = self.NanonisTCP.hex_to_float32(response[16:20])
        end_settling_time     = self.NanonisTCP.hex_to_float32(response[20:24])
        z_control_time        = self.NanonisTCP.hex_to_float32(response[24:28])

        return {"z_averaging_time"      : z_averaging_time,
                "initial_settling_time" : initial_settling_time,
                "maximum_slew_rate"     : maximum_slew_rate,
                "settling_time"         : settling_time,
                "integration_time"      : integration_time,
                "end_settling_time"     : end_settling_time,
                "z_control_time"        : z_control_time}

    def RetractDelaySet(self, retract_delay):
        """
        Sets the Z-spectroscopy retract delay.

        Parameters
        ----------
        retract_delay : Delay in seconds between forward sweep and backward
                        sweep (s)

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.RetractDelaySet', body_size=4)

        ## arguments
        hex_rep += self.NanonisTCP.float32_to_hex(retract_delay)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def RetractDelayGet(self):
        """
        Returns the Z-spectroscopy retract delay.

        Returns
        -------
        retract_delay : Delay in seconds between forward sweep and backward
                        sweep (s)

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.RetractDelayGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response()

        retract_delay = self.NanonisTCP.hex_to_float32(response[0:4])

        return retract_delay

    def RetractSet(self, enable, threshold, signal_index, comparison):
        """
        Sets the configuration for the main condition of the Auto Retract in
        the Z-Spectroscopy module.

        Parameters
        ----------
        enable       : Switches the Auto Retract on or off.
                       0: No change; 1: On; 2: Off
        threshold    : Combined with the comparison, sets which situation
                       triggers the main condition to auto-retract the tip
        signal_index : Index (0-127) of the signal used to check the main
                       retract condition. Use -1 to leave unchanged in Nanonis.
        comparison   : Sets which situation triggers the main condition.
                       0: >; 1: <; 2: No change

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.RetractSet', body_size=12)

        ## arguments
        hex_rep += self.NanonisTCP.to_hex(enable, 2)
        hex_rep += self.NanonisTCP.float32_to_hex(threshold)
        hex_rep += self.NanonisTCP.to_hex(signal_index, 4)
        hex_rep += self.NanonisTCP.to_hex(comparison, 2)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def RetractGet(self):
        """
        Returns the configuration for the main condition of the Auto Retract
        in the Z-Spectroscopy module.

        Returns
        -------
        enable       : 0: Off; 1: On
        threshold    : Combined with the comparison, defines which situation
                       triggers the main condition to auto-retract the tip
        signal_index : Index (0-127) of the signal used to check the main
                       retract condition. -1 means unchanged.
        comparison   : 0: >; 1: <

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.RetractGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response()

        enable       = self.NanonisTCP.hex_to_uint16(response[0:2])
        threshold    = self.NanonisTCP.hex_to_float32(response[2:6])
        signal_index = self.NanonisTCP.hex_to_int32(response[6:10])
        comparison   = self.NanonisTCP.hex_to_uint16(response[10:12])

        return {"enable"       : enable,
                "threshold"    : threshold,
                "signal_index" : signal_index,
                "comparison"   : comparison}

    def Retract2ndSet(self, condition_2nd, threshold, signal_index, comparison):
        """
        Sets the configuration for the 2nd condition of the Auto Retract in
        the Z-Spectroscopy module.

        Parameters
        ----------
        condition_2nd : Configures the use of a second signal comparison.
                        0: No change
                        1: -No- (disables 2nd condition)
                        2: OR  (retract if 1st or 2nd condition met)
                        3: AND (retract if 1st and 2nd met simultaneously)
                        4: THEN (2nd condition only checked after 1st met)
        threshold     : Combined with the comparison, sets which situation
                        triggers the 2nd condition to auto-retract
        signal_index  : Index (0-127) of the signal for the 2nd retract
                        condition. Use -1 to leave unchanged.
        comparison    : 0: >; 1: <; 2: No change

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.Retract2ndSet', body_size=14)

        ## arguments
        hex_rep += self.NanonisTCP.to_hex(condition_2nd, 4)
        hex_rep += self.NanonisTCP.float32_to_hex(threshold)
        hex_rep += self.NanonisTCP.to_hex(signal_index, 4)
        hex_rep += self.NanonisTCP.to_hex(comparison, 2)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def Retract2ndGet(self):
        """
        Returns the configuration for the 2nd condition of the Auto Retract
        in the Z-Spectroscopy module.

        Returns
        -------
        condition_2nd : 0: -No-; 1: OR; 2: AND; 3: THEN
        threshold     : Combined with the comparison, indicates which situation
                        triggers the 2nd condition to auto-retract
        signal_index  : Index (0-127) of the signal for the 2nd retract
                        condition
        comparison    : 0: >; 1: <

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.Retract2ndGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response()

        condition_2nd = self.NanonisTCP.hex_to_int32(response[0:4])
        threshold     = self.NanonisTCP.hex_to_float32(response[4:8])
        signal_index  = self.NanonisTCP.hex_to_int32(response[8:12])
        comparison    = self.NanonisTCP.hex_to_uint16(response[12:14])

        return {"condition_2nd" : condition_2nd,
                "threshold"     : threshold,
                "signal_index"  : signal_index,
                "comparison"    : comparison}

    def DigSyncSet(self, digital_sync):
        """
        Sets the TTL/pulse sequence synchronization option in the Advanced
        section of the Z Spectroscopy module.

        Parameters
        ----------
        digital_sync : 0: No change; 1: Off; 2: TTL Sync; 3: Pulse Sequence

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.DigSyncSet', body_size=2)

        ## arguments
        hex_rep += self.NanonisTCP.to_hex(digital_sync, 2)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def DigSyncGet(self):
        """
        Returns the configured TTL/pulse sequence synchronization option in
        the Advanced section of the Z Spectroscopy module.

        Returns
        -------
        digital_sync : 0: Off; 1: TTL Sync; 2: Pulse Sequence

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.DigSyncGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response()

        digital_sync = self.NanonisTCP.hex_to_uint16(response[0:2])

        return digital_sync

    def TTLSyncSet(self, ttl_line, ttl_polarity, time_to_on, on_duration):
        """
        Sets the configuration of the TTL Synchronization feature in the
        Advanced section of the Z Spectroscopy module.

        Parameters
        ----------
        ttl_line     : Which digital line to control.
                       0: No change; 1: HS Line 1; 2: HS Line 2;
                       3: HS Line 3; 4: HS Line 4
        ttl_polarity : Polarity of the switching action.
                       0: No change; 1: Low Active; 2: High Active
        time_to_on   : Time to wait before activating the TTL line (s)
        on_duration  : How long the TTL line is activated before resetting (s)

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.TTLSyncSet', body_size=12)

        ## arguments
        hex_rep += self.NanonisTCP.to_hex(ttl_line, 2)
        hex_rep += self.NanonisTCP.to_hex(ttl_polarity, 2)
        hex_rep += self.NanonisTCP.float32_to_hex(time_to_on)
        hex_rep += self.NanonisTCP.float32_to_hex(on_duration)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def TTLSyncGet(self):
        """
        Returns the configuration of the TTL Synchronization feature in the
        Advanced section of the Z Spectroscopy module.

        Returns
        -------
        ttl_line     : 0: HS Line 1; 1: HS Line 2; 2: HS Line 3; 3: HS Line 4
        ttl_polarity : 0: Low Active; 1: High Active
        time_to_on   : Time to wait before activating TTL line (s).
                       This time is a multiple of the Real-Time cycle time.
        on_duration  : How long the TTL line is activated before resetting (s).
                       This time is a multiple of the Real-Time cycle time.

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.TTLSyncGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response()

        ttl_line     = self.NanonisTCP.hex_to_uint16(response[0:2])
        ttl_polarity = self.NanonisTCP.hex_to_uint16(response[2:4])
        time_to_on   = self.NanonisTCP.hex_to_float32(response[4:8])
        on_duration  = self.NanonisTCP.hex_to_float32(response[8:12])

        return {"ttl_line"     : ttl_line,
                "ttl_polarity" : ttl_polarity,
                "time_to_on"   : time_to_on,
                "on_duration"  : on_duration}

    def PulseSeqSyncSet(self, pulse_seq_nr, nr_periods):
        """
        Sets the configuration of the pulse sequence synchronization feature
        in the Advanced section of the Z Spectroscopy module.

        Parameters
        ----------
        pulse_seq_nr : Pulse sequence number as configured in the Pulse
                       Generation module. 0 means no change.
        nr_periods   : Number of times the same pulse sequence is executed

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.PulseSeqSyncSet', body_size=6)

        ## arguments
        hex_rep += self.NanonisTCP.to_hex(pulse_seq_nr, 2)
        hex_rep += self.NanonisTCP.to_hex(nr_periods, 4)

        self.NanonisTCP.send_command(hex_rep)

        self.NanonisTCP.receive_response(0)

    def PulseSeqSyncGet(self):
        """
        Returns the configuration of the pulse sequence synchronization
        feature in the Advanced section of the Z Spectroscopy module.

        Returns
        -------
        pulse_seq_nr : Pulse sequence number as configured in the Pulse
                       Generation module
        nr_periods   : Number of times the same pulse sequence is executed

        """
        hex_rep = self.NanonisTCP.make_header('ZSpectr.PulseSeqSyncGet', body_size=0)

        self.NanonisTCP.send_command(hex_rep)

        response = self.NanonisTCP.receive_response()

        pulse_seq_nr = self.NanonisTCP.hex_to_uint16(response[0:2])
        nr_periods   = self.NanonisTCP.hex_to_uint32(response[2:6])

        return {"pulse_seq_nr" : pulse_seq_nr,
                "nr_periods"   : nr_periods}
