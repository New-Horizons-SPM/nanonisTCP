# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 14:56:45 2023

@author: jced0001
"""
import numpy as np

class Osci2T:
    """
    Nanonis Oscilloscope 2-Channels Module
    """
    def __init__(self,NanonisTCP):
        self.NanonisTCP = NanonisTCP

    def Run(self):
        """
        Starts the Oscilloscope 2-Channels Module
        
        This module does not run when its front panel is closed. To automate 
        measurements it is required to run the module first using this function
    

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Osci2T.Run', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def ChsSet(self,chA=-1,chB=-1):
        """
        Sets the channels to display in the Oscilloscope 2-Channels. Leaving 
        chA or chB as -1 will leave the setting as is in Nanonis

        Parameters
        ----------
        chA : Sets the channel A, where chA is comprised between 0 and 23, and 
              it corresponds to the list of signals assigned to the 24 slots in
              the Signals Manager.
              To get the signal name and its corresponding index in the list of
              the 128 available signals in the nanonis controller use the 
              Signals.InSlotsGet function
        chB : sets the channel B where the in index is comprised between 0 and 
              23, and it corresponds to the list of signals assigned to the 24
              slots in the Signals Manager

        """
        chA_temp,chB_temp = self.ChsGet()
        if(chA == -1): chA = chA_temp
        if(chB == -1): chB = chB_temp
        
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Osci2T.ChsSet', body_size=8)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(chA,4)
        hex_rep += self.NanonisTCP.to_hex(chB,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def ChsGet(self):
        """
        Returns the channels displayed in the Oscilloscope 2-Channels

        Returns
        -------
        chA : Returns channel A, where chA is comprised between 0 and 23, and 
              it corresponds to the list of signals assigned to the 24 slots in
              the Signals Manager.
              To get the signal name and its corresponding index in the list of
              the 128 available signals in the nanonis controller use the 
              Signals.InSlotsGet function
        chB : Returns channel B where the in index is comprised between 0 and 
              23, and it corresponds to the list of signals assigned to the 24
              slots in the Signals Manager

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Osci2T.ChsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        chA = self.NanonisTCP.hex_to_uint16(response[0:4])
        chB = self.NanonisTCP.hex_to_uint16(response[4:8])
        
        return [chA,chB]
    
    def TimebaseSet(self,timebaseIndex):
        """
        Sets the timebase in the Oscilloscope 2-Channels.
        To set the timebase, use the Osci2T.TimebaseGet function first to 
        obtain a list of available timebases. Then, use the index of the 
        desired timebase as input to this function.
        The available timebases depend on the RT frequency and the RT 
        oversampling.

        Parameters
        ----------
        timebaseIndex : Timebase index

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Osci2T.TimebaseSet', body_size=2)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(timebaseIndex,2)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def TimebaseGet(self):
        """
        Returns the timebase in the Oscilloscope 2-Channels.
        The available timebases depend on the RT frequency and the RT 
        oversampling.

        Returns
        -------
        timebaseIndex : Timebase index
        timebases : returns an array of the timebsaes values in seconds

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Osci2T.TimebaseGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        timebaseIndex = self.NanonisTCP.hex_to_int16(response[0:2])
        numTimebases  = self.NanonisTCP.hex_to_int32(response[2:6])
        
        idx = 6
        timebases = []
        for n in range(numTimebases):
            timebases.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
            idx += 4
        
        return [timebaseIndex,np.array(timebases)]
    
    def OversamplSet(self,oversamplingIndex):
        """
        Sets the oversampling in the Oscilloscope 2-Channels

        Parameters
        ----------
        oversamplingIndex : defines how many integer number of samples each 
                            data point is averaged over. Index 0 means 50 
                            samples, index 1 means 20, index 2 means 10, index 
                            3 means 5, index 4 means 2, and index 5 means 1 
                            sample (so no averaging)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Osci2T.OversamplSet', body_size=2)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(oversamplingIndex,2)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def OversamplGet(self):
        """
        Returns the oversampling in the Oscilloscope 2-Channels

        Returns
        -------
        oversamplingIndex : defines how many integer number of samples each 
                            data point is averaged over. Index 0 means 50 
                            samples, index 1 means 20, index 2 means 10, index 
                            3 means 5, index 4 means 2, and index 5 means 1 
                            sample (so no averaging)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Osci2T.OversamplGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(2)
        
        oversamplingIndex = self.NanonisTCP.hex_to_int16(response[0:2])
        
        return oversamplingIndex
    
    def TrigSet(self,mode,channel,slope,level,hysteresis,position):
        """
        Sets the trigger configuration in Oscilloscope 2-Channels

        Parameters
        ----------
        mode        : sets the trigger mode. For Immediate mode, no further 
                      config is required.
                      0 : Immediate mode
                      1 : Level mode
                      2 : Auto mode
              
        channel     : sets the channel used to trigger
                      0 : chA
                      1 : chB
        slope       : sets whether to trigger on rising or falling slope
                      0 : falling
                      1 : rising
        level       : sets the value the signal must cross (in the directin of
                      the slope specified) to trigger
        hysteresis  : is used to prevent noise from causing a false trigger.
                      For a rising edge trigger, the signal must pass below
                      (level - hysteresis) before a trigger level crossing is
                      detected
                      For a falling edge trigger, the signal must pass above
                      (level + hysteresis) before a trigger level crossing is
                      detected
        position    : sets the pre-sampling trigger position in seconds

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Osci2T.TrigSet', body_size=30)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(mode,2)
        hex_rep += self.NanonisTCP.to_hex(channel,2)
        hex_rep += self.NanonisTCP.to_hex(slope,2)
        hex_rep += self.NanonisTCP.float64_to_hex(level)
        hex_rep += self.NanonisTCP.float64_to_hex(hysteresis)
        hex_rep += self.NanonisTCP.float64_to_hex(position)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def TrigGet(self):
        """
        

        Returns
        -------
        mode        : Returns the trigger mode.
                      0 : Immediate mode
                      1 : Level mode
                      2 : Auto mode
              
        channel     : returns the channel used to trigger
                      0 : chA
                      1 : chB
        slope       : returns whether to trigger on rising or falling slope
                      0 : falling
                      1 : rising
        level       : returns the value the signal must cross (in the directin 
                      of the slope specified) to trigger
        hysteresis  : is used to prevent noise from causing a false trigger.
                      For a rising edge trigger, the signal must pass below
                      (level - hysteresis) before a trigger level crossing is
                      detected
                      For a falling edge trigger, the signal must pass above
                      (level + hysteresis) before a trigger level crossing is
                      detected
        position    : returns the pre-sampling trigger position in seconds

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Osci2T.TrigGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(30)
        
        mode        = self.NanonisTCP.hex_to_int16(response[0:2])
        channel     = self.NanonisTCP.hex_to_int16(response[2:4])
        slope       = self.NanonisTCP.hex_to_int16(response[4:6])
        level       = self.NanonisTCP.hex_to_float64(response[6:14])
        hysteresis  = self.NanonisTCP.hex_to_float64(response[14:22])
        position    = self.NanonisTCP.hex_to_float64(response[22:30])
        
        return [mode,channel,slope,level,hysteresis,position]
    
    def DataGet(self,dataToGet):
        """
        Returns the graph data from the Oscilloscope 2-Channels

        Parameters
        ----------
        dataToGet : 'Current' returns the currently displayed data. 'Next' 
                    waits for the next trigger to retrieve data. 'Wait' waits
                    two triggers
                    0 : Current
                    1 : Next
                    2 : Wait
        Returns
        -------
        t0  : timestamp of the first acquired point
        dt  : time distance between two acquired points
        chA : numpy array of chA data
        chB : numpy array of chB data

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Osci2T.DataGet', body_size=2)
        
        hex_rep += self.NanonisTCP.to_hex(dataToGet,2)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        t0  = self.NanonisTCP.hex_to_float64(response[0:8])
        dt  = self.NanonisTCP.hex_to_float64(response[8:16])
        pts = self.NanonisTCP.hex_to_int32(response[16:20])
        
        idx = 20
        chA = []
        for n in range(pts):
            chA.append(self.NanonisTCP.hex_to_float64(response[idx:idx+8]))
            idx += 8
        
        chB = []
        for n in range(pts):
            chB.append(self.NanonisTCP.hex_to_float64(response[idx:idx+8]))
            idx += 8
            
        return [t0,dt,np.array(chA),np.array(chB)]
        