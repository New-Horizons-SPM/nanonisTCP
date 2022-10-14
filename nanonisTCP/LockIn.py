# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 20:29:16 2022

@author: jced0001
"""

class LockIn:
    """
    Nanonis LockIn Module
    """
    def __init__(self,NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def ModOnOffSet(self,modulator_number,lockin_onoff):
        """
        Turns the specified Lock-In modulator on or off.

        Parameters
        ----------
        modulator_number : The number that specifies which modulator to use. 
                           It starts from number 1 (=Modulator 1)
        lockin_onoff     : Turns the specified modulator on or off, where 0=Off
                           and 1=On

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModOnOffSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        hex_rep += self.NanonisTCP.to_hex(lockin_onoff,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def ModOnOffGet(self,modulator_number):
        """
        Returns if the specified Lock-In modulator is turned on or off.

        Parameters
        ----------
        modulator_number : The number that specifies which modulator to use. 
                           It starts from number 1 (=Modulator 1)

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModOnOffGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        lockin_onoff = self.NanonisTCP.hex_to_uint32(response[0:4])
        
        return lockin_onoff
    
    def ModSignalSet(self,modulator_number,modulator_signal_index):
        """
        Selects the modulated signal of the specified Lock-In modulator.

        Parameters
        ----------
        modulator_number : the number that specifies which modulator to use.
                           It starts from number 1 (=Modulator 1)
        modulator_signal_index : the signal index out of the list of 128 signals
                           available in the software.
                           To get a list of the available signals, use the
                           Signals.NamesGet function.

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModSignalSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        hex_rep += self.NanonisTCP.to_hex(modulator_signal_index,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def ModSignalGet(self,modulator_number):
        """
        Returns the modulated signal of the specified Lock-In modulator.

        Returns
        -------
        modulator_signal_index : the signal index out of the list of 128 signals
                          available in the software.
                          To get a list of the available signals, use the 
                          Signals.NamesGet function.

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModSignalGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        modulator_signal_index = self.NanonisTCP.hex_to_uint32(response[0:4])
        
        return modulator_signal_index
    
    def ModPhasRegSet(self,modulator_number,phase_register_index):
        """
        Sets the phase register index of the specified Lock-In modulator.
        Each modulator can work on any phase register (frequency). Use this 
        function to assign the modulator to one of the 8 available phase
        registers (index 1-8). Use the LockIn.ModPhaFreqSet function to set the
        frequency of the phase registers.
        
        Parameters
        ----------
        modulator_number : the number that specifies which modulator to use.
                           It starts from number 1. (=Modulator 1)
        phase_register_index : the index of the phase register of the specified
                               Lock-In modulator. Valid values are index 1 to 8
                              
        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModPhasRegSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        hex_rep += self.NanonisTCP.to_hex(phase_register_index,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def ModPhasRegGet(self,modulator_number):
        """
        Returns the phase register index of the specified Lock-In modulator.
        Each modulator can work on any phase register (frequency generator).
        Use the LockIn.ModPhaseRegFreqGet function to get the frequency of the 
        phase registers.

        Parameters
        ----------
        modulator_number : the number that specifies which modulator to use.
                           It starts from number 1. (=Modulator 1)

        Returns
        -------
        phase_register_index : the index of the phase register of the specified
                               Lock-In modulator. Valid values are index 1 to 8
        

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModPhasRegGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        phase_register_index = self.NanonisTCP.hex_to_uint32(response[0:4])
        
        return phase_register_index
    
    def ModHarmonicSet(self,modulator_number,harmonic):
        """
        Sets the harmonic of the specified Lock-In modulator.
        The modulator is bound to a phase register (frequency generator), but 
        it can work on harmonics. Harmonic 1 is the base frequency (the 
        frequency of the frequency generator).

        Parameters
        ----------
        modulator_number : the number that specifies which modulator to use.
                           It starts from number 1. (=Modulator 1)
        harmonic         : the harmonic of the specified Lock-In modulator.
                           Valid values start from 1 (=base frequency)

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModHarmonicSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        hex_rep += self.NanonisTCP.to_hex(harmonic,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def ModHarmonicGet(self,modulator_number):
        """
        Returns the harmonic of the specified Lock-In modulator.
        The modulator is bound to a phase register (frequency generator), but 
        it can work on harmonics. Harmonic 1 is the base frequency (the 
        frequency of the frequency generator).

        Parameters
        ----------
        modulator_number : the number that specifies which modulator to use.
                           It starts from number 1. (=Modulator 1)

        Returns
        -------
        harmonic         : the harmonic of the specified Lock-In modulator.
                           Valid values start from 1 (=base frequency)

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModHarmonicGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        harmonic = self.NanonisTCP.hex_to_uint32(response[0:4])
        
        return harmonic
    
    def ModPhasSet(self,modulator_number,phase_deg):
        """
        Sets the modulation phase offset of the specified Lock-In modulator.

        Parameters
        ----------
        modulator_number : the number that specifies which modulator to use.
                           It starts from number 1. (=Modulator 1)
        phase_deg        : the modulation phase offset of the specified Lock-In
                           modulator

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModPhasSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        hex_rep += self.NanonisTCP.float32_to_hex(phase_deg)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def ModPhasGet(self,modulator_number):
        """
        Returns the modulation phase offset of the specified Lock-In modulator.

        Parameters
        ----------
        modulator_number : the number that specifies which modulator to use.
                           It starts from number 1. (=Modulator 1)

        Returns
        -------
        phase_deg        : the modulation phase offset of the specified Lock-In
                           modulator

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModPhasGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        phase_deg = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return phase_deg
    
    def ModAmpSet(self,modulator_number,amplitude):
        """
        Sets the modulation amplitude of the specified Lock-In modulator.
        
        Parameters
        ----------
        modulator_number : the number that specifies which modulator to use.
                           It starts from number 1. (=Modulator 1)
        amplitude        : the modulation amplitude of the specified Lock-In 
                           modulator

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModAmpSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        hex_rep += self.NanonisTCP.float32_to_hex(amplitude)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def ModAmpGet(self,modulator_number):
        """
        Returns the modulation amplitude of the specified Lock-In modulator.

        Parameters
        ----------
        modulator_number : the number that specifies which modulator to use.
                           It starts from number 1. (=Modulator 1)

        Returns
        -------
        amplitude        : the modulation amplitude of the specified Lock-In 
                           modulator

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModAmpGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        amplitude = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return amplitude
        
    def ModPhasFreqSet(self,modulator_number,frequency):
        """
        Sets the frequency of the specified Lock-In phase register/modulator.
        The Lock-in module has a total of 8 frequency generators / phase 
        registers. Each modulator and demodulator can be bound to one of the 
        phase registers.
        This function sets the frequency of one of the phase registers.

        Parameters
        ----------
        modulator_number : the number that specifies which modulator to use.
                           It starts from number 1. (=Modulator 1)
        frequency        : the frequency of the specified Lock-In phase 
                           register (Hz)

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModPhasFreqSet', body_size=12)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        hex_rep += self.NanonisTCP.float64_to_hex(frequency)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def ModPhasFreqGet(self,modulator_number):
        """
        Returns the frequency of the specified Lock-In phase register/modulator
        The Lock-in module has a total of 8 frequency generators / phase 
        registers. Each modulator and demodulator can be bound to one of the 
        phase registers.
        This function gets the frequency of one of the phase registers.

        Parameters
        ----------
        modulator_number : the number that specifies which modulator to use.
                           It starts from number 1. (=Modulator 1)

        Returns
        -------
        frequency        : the frequency of the specified Lock-In phase 
                           register (Hz)

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.ModPhasFreqGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(modulator_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        frequency = self.NanonisTCP.hex_to_float64(response[0:8])
        
        return frequency