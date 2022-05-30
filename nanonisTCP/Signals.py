# -*- coding: utf-8 -*-
"""
Created on Mon May 30 12:33:59 2022

@author: Julian Ceddia
"""

class Signals:
    """
    Nanonis Signals Module
    """
    def __init__(self,NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def NamesGet(self):
        """
        Returns the signals names list of the 128 signals available in the 
        software

        Returns
        -------
        signal_names : String array of signal names

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Signals.NamesGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        # signals_names_size = self.NanonisTCP.hex_to_int32(response[0:4])
        signals_names_num  = self.NanonisTCP.hex_to_int32(response[4:8])
        
        idx = 8
        signal_names = []
        for n in range(signals_names_num):
            size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            signal_name = response[idx:idx+size].decode()
            idx += size
            signal_names.append(signal_name)
        
        return signal_names
    
    def InSlotSet(self,slot,RTSignalIndex):
        """
        Assigns one of the 128 available signals to one of the 24 slots of the 
        Signals Manager.

        Parameters
        ----------
        slot          : The index of the slot in the Signals Manager where one 
                        of the 128 RT signals is assigned, so that index could 
                        be any value from 0 to 23
        RTSignalIndex : The index of the RT signal to assign to the selected 
                        slot, so that index could be any value from 0 to 127

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Signals.InSlotSet', body_size=8)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(slot,4)
        hex_rep += self.NanonisTCP.to_hex(RTSignalIndex,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def InSlotsGet(self):
        """
        Returns a list of the signals names and indexes of the 24 signals 
        assigned to the slots of the Signals Manager.
        
        The 24 signals are selected in the Signals Manager out of the 128 
        signals available in the software, and they are used in the list of 
        available signals to display in graphs and other modules.
        
        The index of every signal corresponds to the index in the list of 128 
        signals (0-127). The latter can be returned by Signals.NamesGet.

        Returns
        -------
        signal_names   : Str array of selected signal names
        signal_indexes : Int array of signal indexes

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Signals.InSlotsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        # signals_names_size = self.NanonisTCP.hex_to_int32(response[0:4])
        signals_names_num  = self.NanonisTCP.hex_to_int32(response[4:8])
        
        idx = 8
        signal_names = []
        for n in range(signals_names_num):
            size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            signal_name = response[idx:idx+size].decode()
            idx += size
            signal_names.append(signal_name)
        
        signal_indexes = []
        signal_indexes_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        for n in range(signal_indexes_size):
            idx += 4
            signal_index = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            signal_indexes.append(signal_index)
            
        return [signal_names,signal_indexes]
    
    def CalibrGet(self,signal_index):
        """
        Returns the calibration and offset of the selected signal.

        Parameters
        ----------
        signal_index : Index of the signal to retrieve calibration for (0-127)

        Returns
        -------
        calibration : signal calibration (V^-1)
        offset      : signal offset in physical units

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Signals.CalibrGet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(signal_index,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(8)
        
        calibration = self.NanonisTCP.hex_to_float32(response[0:4])
        offset      = self.NanonisTCP.hex_to_float32(response[4:8])
        
        return [calibration,offset]
    
    def RangeGet(self,signal_index):
        """
        Returns the range limits of the selected signal

        Parameters
        ----------
        signal_index : Index of the signal to retrieve range for

        Returns
        -------
        max_limit: range max
        min_limit: range min

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Signals.RangeGet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(signal_index,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(8)
        
        max_limit = self.NanonisTCP.hex_to_float32(response[0:4])
        min_limit = self.NanonisTCP.hex_to_float32(response[4:8])
        
        return [max_limit,min_limit]
    
    def ValGet(self,signal_index,wait_for_newest_data=True):
        """
        Returns the current value of the selected signal (oversampled during 
        the Acquisition Period time, Tap).
        
        Signal measurement principle:
        The signal is continuously oversampled with the Acquisition Period
        time, Tap, specified in the TCP receiver module. Every Tap second, the 
        oversampled data is "published". This VI function waits for the next 
        oversampled data to be published and returns its value. Calling this 
        function does not trigger a signal measurement; it waits for data to be
        published! Thus, this function returns a value 0 to Tap second after
        being called.
        
        An important consequence is that if you change a signal and immediately
        call this function to read a measurement you might get "old" data
        (i.e. signal data measured before you changed the signal).
        The solution to get only new data is to set Wait for newest data to
        True. In this case, the first published data is discarded and only the
        second one is returned.

        Parameters
        ----------
        signal_index         : Index of the signal to retrieve a value for
        wait_for_newest_data : Selects whether the function returns the next
                               available signal value or if it waits for a full
                               period of new data. If False, this function
                               returns a value 0 to Tap seconds after being
                               called. If True, the function discard the first
                               oversampled signal value received but returns
                               the second value received. Thus, the function
                               returns a value Tap to 2*Tap seconds after being
                               called. It could be 0=False or 1=True

        Returns
        -------
        signal_value : The value of the selected signal in physical units

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Signals.ValGet', body_size=8)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(signal_index,4)
        hex_rep += self.NanonisTCP.to_hex(wait_for_newest_data,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(8)
        
        signal_value = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return signal_value