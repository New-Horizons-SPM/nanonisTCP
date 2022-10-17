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
    
    def DemodSignalSet(self,demod_number,demod_signal_index):
        """
        Selects the demodulated signal of the specified Lock-In demodulator.

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)
        demod_signal_index : The signal index out of the list of 128 signals
                             available in the software.
                             To get a list of the available signals, use the 
                             Signals.NamesGet function.

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodSignalSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        hex_rep += self.NanonisTCP.to_hex(demod_signal_index,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def DemodSignalGet(self,demod_number):
        """
        Returns the demodulated signal of the specified Lock-In demodulator.

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)

        Returns
        -------
        demod_signal_index : The signal index out of the list of 128 signals
                             available in the software.
                             To get a list of the available signals, use the 
                             Signals.NamesGet function.

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodSignalGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        demod_signal_index = self.NanonisTCP.hex_to_int(response[0:4])
        
        return demod_signal_index
        
    def DemodHarmonicSet(self,demod_number,harmonic):
        """
        Sets the harmonic of the specified Lock-In demodulator.
        The demodulator demodulates the input signal at the specified harmonic
        overtone of the frequency generator. Harmonic 1 is the base frequency
        (the frequency of the frequency generator).

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)
        harmonic : The harmonic of the specified Lock-In demodulator. Valid 
                   values start from 1 (=base frequency)

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodHarmonicSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        hex_rep += self.NanonisTCP.to_hex(harmonic,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def DemodHarmonicGet(self,demod_number):
        """
        Returns the harmonic of the specified Lock-In demodulator.
        The demodulator demodulates the input signal at the specified harmonic
        overtone of the frequency generator. Harmonic 1 is the base frequency 
        (the frequency of the frequency generator).

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)

        Returns
        -------
        harmonic : The harmonic of the specified Lock-In demodulator. Valid 
                   values start from 1 (=base frequency)

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodHarmonicGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        harmonic = self.NanonisTCP.hex_to_int(response[0:4])
        
        return harmonic
    
    def DemodHPFilterSet(self,demod_number,hp_filter_order,cutoff):
        """
        Sets the properties of the high-pass filter applied to the demodulated 
        signal of the specified demodulator.
        
        The high-pass filter is applied on the demodulated signal before the
        actual demodulation. It is used to get rid of DC or low-frequency 
        components which could result in undesired components close to the 
        modulation frequency on the demodulator output signals (X,Y).

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)
        hp_filter_order : The high-pass filter order. Valid values are from 
                          -1 to 8.
                          -1 = no change
                           0 = filter off.
        cutoff :    high-pass filter cutoff frequency in Hz, where 0 = no change.

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodHPFilterSet', body_size=12)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        hex_rep += self.NanonisTCP.to_hex(hp_filter_order,4)
        hex_rep += self.NanonisTCP.float32_to_hex(cutoff)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def DemodHPFilterGet(self,demod_number):
        """
        Returns the properties of the high-pass filter applied to the 
        demodulated signal of the specified demodulator.
        
        The high-pass filter is applied on the demodulated signal before the
        actual demodulation. It is used to get rid of DC or low-frequency 
        components which could result in undesired components close to the 
        modulation frequency on the demodulator output signals (X,Y).

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)

        Returns
        -------
        hp_filter_order : The high-pass filter order. Valid values are from 
                          0 to 8.
                          0 = filter off.
        cutoff :    high-pass filter cutoff frequency in Hz.

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodHPFilterGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        hp_filter_order = self.NanonisTCP.hex_to_int(response[0:4])
        cutoff          = self.NanonisTCP.hex_to_float32(response[4:8])
        
        return {"hp_filter_order" : hp_filter_order,
                "cutoff": cutoff}
    
    def DemodLPFilterSet(self,demod_number,lp_filter_order,cutoff):
        """
        Sets the properties of the low-pass filter applied to the demodulated
        signal of the specified demodulator.
        
        The low-pass filter is applied on the demodulator output signals (X,Y) 
        to remove undesired components. Lower cut-off frequency means better
        suppression of undesired frequency components, but longer response time
        (time constant) of the filter.

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)
        lp_filter_order : The low-pass filter order. Valid values are from 
                          -1 to 8.
                          -1 = no change
                           0 = filter off
        cutoff : low-pass filter cutoff frequency in Hz
                 0 = no change

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodLPFilterSet', body_size=12)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        hex_rep += self.NanonisTCP.to_hex(lp_filter_order,4)
        hex_rep += self.NanonisTCP.float32_to_hex(cutoff)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def DemodLPFilterGet(self,demod_number):
        """
        Returns the properties of the low-pass filter applied to the
        demodulated signal of the specified demodulator.
        
        The low-pass filter is applied on the demodulator output signals (X,Y) 
        to remove undesired components. Lower cut-off frequency means better 
        suppression of undesired frequency components, but longer response time 
        (time constant) of the filter.

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)

        Returns
        -------
        lp_filter_order : The low-pass filter order. Valid values are from 
                          0 to 8.
                          0 = filter off
        cutoff : low-pass filter cutoff frequency in Hz

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodLPFilterGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        lp_filter_order = self.NanonisTCP.hex_to_int(response[0:4])
        cutoff          = self.NanonisTCP.hex_to_float32(response[4:8])
        
        return {"lp_filter_order" : lp_filter_order,
                "cutoff": cutoff}
    
    def DemodPhasRegSet(self,demod_number,phase_register_index):
        """
        

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)
        phase_register_index : The index of the phase register of the specified 
                               Lock-In demodulator. Valid values are index 
                               1 to 8.

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodPhasRegSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        hex_rep += self.NanonisTCP.to_hex(phase_register_index,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def DemodPhasRegGet(self,demod_number):
        """
        Returns the phase register index of the specified Lock-In demodulator.
        Each demodulator can work on any phase register (frequency). Use the 
        LockIn.ModPhaFreqSet function to set the frequency of the phase 
        registers.

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)

        Returns
        -------
        phase_register_index : The index of the phase register of the specified 
                               Lock-In demodulator. Valid values are index 
                               1 to 8.

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodPhasRegGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        phase_register_index = self.NanonisTCP.hex_to_int(response[0:4])
        
        return phase_register_index
    
    def DemodPhasSet(self,demod_number,phase_deg):
        """
        Sets the reference phase of the specified Lock-In demodulator.

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)
        phase_deg : is the reference phase of the specified Lock-In demodulator

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodPhasSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        hex_rep += self.NanonisTCP.float32_to_hex(phase_deg)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def DemodPhasGet(self,demod_number):
        """
        Returns the reference phase of the specified Lock-In demodulator.

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)

        Returns
        -------
        phase_deg : is the reference phase of the specified Lock-In demodulator

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodPhasGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        phase_deg = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return phase_deg
    
    def DemodSyncFilterSet(self,demod_number,sync_filter):
        """
        Switches the synchronous (Sync) filter of the specified demodulator 
        On or Off.
        
        The synchronous filter is applied on the demodulator output signals 
        (X,Y) after the low-pass filter. It is very good in suppressing 
        harmonic components (harmonics of the demodulation frequency), but does 
        not suppress other frequencies.
        
        The sync filter does not output a continuous signal, it only updates 
        the value after each period of the demodulation frequency.

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)
        sync_filter : The synchronous filter of the specified demodulator on 
                      or off.
                      0 = Off
                      1 = On

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodSyncFilterSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        hex_rep += self.NanonisTCP.to_hex(sync_filter,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def DemodSyncFilterGet(self,demod_number):
        """
        Returns the status (on/off) of the synchronous (Sync) filter of the
        specified demodulator.
        
        The synchronous filter is applied on the demodulator output signals 
        (X,Y) after the low-pass filter. It is very good in suppressing 
        harmonic components (harmonics of the demodulation frequency), but does
        not suppress other frequencies.
        
        The sync filter does not output a continuous signal, it only updates 
        the value after each period of the demodulation frequency.

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)

        Returns
        -------
        sync_filter : The synchronous filter of the specified demodulator on 
                      or off.
                      0 = Off
                      1 = On

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodSyncFilterGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        sync_filter = self.NanonisTCP.hex_to_uint32(response[0:4])
        
        return sync_filter
    
    def DemodRTSignalsSet(self,demod_number,rt_signals):
        """
        Sets the signals available for acquisition on the real-time system from 
        the specified demodulator

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)
        rt_signals : sets which signals from the specified demodulator should 
                     be available on the Real-time system. 
                     0 = sets the available 
                     RT Signals to X/Y
                     1 = sets them to R/phi

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodRTSignalsSet', body_size=8)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        hex_rep += self.NanonisTCP.to_hex(rt_signals,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def DemodRTSignalsGet(self,demod_number):
        """
        Returns which the signals are available for acquisition on the 
        real-time system from the specified demodulator.

        Parameters
        ----------
        demod_number : The number that specifies which demodulator to use. It 
                       starts from number 1 (=Demodulator 1)

        Returns
        -------
        rt_signals : Returns which signals from the specified demodulator 
                     should be available on the Real-time system. 
                     0 = X/Y
                     1 = R/phi

        """
        hex_rep = self.NanonisTCP.make_header('LockIn.DemodRTSignalsGet', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(demod_number,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        rt_signals = self.NanonisTCP.hex_to_uint32(response[0:4])
        
        return rt_signals