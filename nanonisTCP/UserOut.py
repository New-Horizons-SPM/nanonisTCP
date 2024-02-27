# -*- coding: utf-8 -*-
"""
Created on Tue Feb 2 18:49:58 2024

@author: jced0001
"""

class UserOut:
    """
    Nanonis User Outputs Module
    """
    def __init__(self, nanonisTCP):
        self.nanonisTCP = nanonisTCP
    
    def ModeSet(self, output_index, output_mode):
        """
        Sets the mode (User Output, Monitor, Calculated signal) of the selected user output channel.

        Parameters
        Output index (int) : Sets the output to be used, where index could be any value from 1 to the number of available outputs
        Output mode (unsigned int16) : Sets the output mode of the selected output, where 0=User Output, 1=Monitor, 2=Calc.Signal
        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.ModeSet', body_size=6)
        
        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        hex_rep += self.nanonisTCP.to_hex(output_mode,2)
        
        self.nanonisTCP.send_command(hex_rep)
        
        self.nanonisTCP.receive_response(0)
    
    def ModeGet(self, output_index):
        """
        Returns the mode (User Output, Monitor, Calculated signal) of the selected user output channel.

        Parameters
        Output index (int) : Sets the output to be used, where index could be any value from 1 to the number of available outputs

        Returns
        Output mode (unsigned int16) : Returns the output mode of the selected output, where 0=User Output, 1=Monitor, 2=Calc.Signal, 3=Override

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.ModeGet', body_size=4)

        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        
        self.nanonisTCP.send_command(hex_rep)
        
        response = self.nanonisTCP.receive_response(2)
        
        output_mode = self.nanonisTCP.hex_to_uint16(response[0:2])
        return output_mode

    def MonitorChSet(self, output_index, monitor_channel_index):
        """
        Sets the monitor channel of the selected output channel.

        Parameters
        Output index (int) : Sets the output to be used, where index could be any value from 1 to the number of available outputs
        Monitor channel index (int) : Sets the index of the channel to monitor.
                                      The index is comprised between 0 and 127 for the physical inputs, physical outputs, and internal channels.
                                      To see which signal has which index, see Signals.NamesGet function.
        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.MonitorChSet', body_size=8)
        
        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        hex_rep += self.nanonisTCP.to_hex(monitor_channel_index,4)
        
        self.nanonisTCP.send_command(hex_rep)
        
        self.nanonisTCP.receive_response(0)
        
    def MonitorChGet(self, output_index):
        """
        Returns the monitor channel of the selected output channel.

        Parameters
        Output index (int) : Sets the output to be used, where index could be any value from 1 to the number of available outputs

        Returns
        Monitor channel index (int): Returns the index of the channel to monitor.
                                     The index is comprised between 0 and 127 for the physical inputs, physical outputs, and internal channels.
                                     To see which signal has which index, see Signals.NamesGet function.

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.MonitorChGet', body_size=4)

        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        
        self.nanonisTCP.send_command(hex_rep)
        
        response = self.nanonisTCP.receive_response(4)
        
        monitor_channel_index = self.nanonisTCP.hex_to_int32(response[0:4])
        return monitor_channel_index
    
    def ValSet(self, output_index, output_value):
        """
        Sets the value of the selected user output channel.

        Parameters
        Output index (int) : Sets the output to be used, where index could be any value from 1 to the number of available outputs
        Output value (float32) : Is the value applied to the selected user output in physical units
        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.ValSet', body_size=8)
        
        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        hex_rep += self.nanonisTCP.float32_to_hex(output_value)
        
        self.nanonisTCP.send_command(hex_rep)
        
        self.nanonisTCP.receive_response(0)
        
    def CalibrSet(self, output_index, calibration, offset):
        """
        Sets the calibration of the selected user output or monitor channel.

        Parameters
        Output index (int) : Sets the output to be used, where index could be any value from 1 to the number of available outputs
        Calibration per volt (float32)
        Offset in physical units (float32)
        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.CalibrSet', body_size=12)
        
        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        hex_rep += self.nanonisTCP.float32_to_hex(calibration)
        hex_rep += self.nanonisTCP.float32_to_hex(offset)
        
        self.nanonisTCP.send_command(hex_rep)
        
        self.nanonisTCP.receive_response(0)

    def CalcSignalNameSet(self, output_index, calculated_signal_name):
        """
        Sets the Calculated Signal name of the selected output channel.

        Parameters
        Output index (int) : Sets the output to be used, where index could be any value from 1 to the number of available outputs
        Calculated signal name (string) is the name of the calculated signal configured for the selected output
        """
        calculated_signal_name_size = int(len(self.nanonisTCP.string_to_hex(calculated_signal_name))/2)
        body_size = 8 + calculated_signal_name_size
        
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.CalcSignalNameSet', body_size=body_size)
        
        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        hex_rep += self.nanonisTCP.to_hex(calculated_signal_name_size,4)
        if(calculated_signal_name_size > 0):
            hex_rep += self.nanonisTCP.string_to_hex(calculated_signal_name)
        
        self.nanonisTCP.send_command(hex_rep)
        
        self.nanonisTCP.receive_response(0)

    
    def CalcSignalNameGet(self, output_index):
        """
        Returns the Calculated Signal name of the selected output channel.

        Parameters
        Output index (int) : Sets the output to be used, where index could be any value from 1 to the number of available outputs

        Returns
        Calculated signal name (string) is the name of the calculated signal configured for the selected output

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.CalcSignalNameGet', body_size=4)

        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        
        self.nanonisTCP.send_command(hex_rep)
        
        response = self.nanonisTCP.receive_response()
        
        calculated_signal_name = ""
        calculated_signal_name_size = self.nanonisTCP.hex_to_int32(response[0:4])
        if(calculated_signal_name_size > 0):
            calculated_signal_name = response[4:4+calculated_signal_name_size].decode()

        return calculated_signal_name
    
    def CalcSignalConfigSet(self, output_index, signal_1, operation, signal_2):
        """
        Sets the configuration of the Calculated Signal for the selected output channel
        The configuration is a math operation between 2 signals, or the logarithmic value of one signal.
        The possible values for the math operation are:
        0=None, 1=Add, 2=Subtract, 3=Multiply, 4=Divide, 6=Log

        Parameters
            Output index (int):          sets the output to be used, where index could be any value from 1 to the number of available outputs
            Signal 1 (unsigned int16):   is the signal index (from 0 to 127) used as the first signal of the formula.
            Operation (unsigned int16):  is the math operation.
            Signal 2 (unsigned int16):   is the signal index (from 0 to 127) used as the second signal of the formula.
        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.CalcSignalConfigSet', body_size=10)
        
        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        hex_rep += self.nanonisTCP.to_hex(signal_1,2)
        hex_rep += self.nanonisTCP.to_hex(operation,2)
        hex_rep += self.nanonisTCP.to_hex(signal_2,2)
        
        self.nanonisTCP.send_command(hex_rep)
        
        self.nanonisTCP.receive_response(0)
        
    def CalcSignalConfigGet(self, output_index):
        """
        Returns the configuration of the Calculated Signal for the selected output channel.
        The configuration is a math operation between 2 signals, or the logarithmic value of one signal.
        The possible values for the math operation are:
        0=None, 1=Add, 2=Subtract, 3=Multiply, 4=Divide, 6=Log

        Parameters
            Output index (int) : Sets the output to be used, where index could be any value from 1 to the number of available outputs

        Returns
            Signal 1 (unsigned int16):   is the signal index (from 0 to 127) used as the first signal of the formula.
            Operation (unsigned int16):  is the math operation.
            Signal 2 (unsigned int16):   is the signal index (from 0 to 127) used as the second signal of the formula.

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.CalcSignalConfigGet', body_size=4)

        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        
        self.nanonisTCP.send_command(hex_rep)
        
        response = self.nanonisTCP.receive_response()
        
        signal_1  = self.nanonisTCP.hex_to_uint16(response[0:2])
        operation = self.nanonisTCP.hex_to_uint16(response[2:4])
        signal_2  = self.nanonisTCP.hex_to_uint16(response[4:6])

        return [signal_1, operation, signal_2]
    
    def LimitsSet(self, output_index, upper_limit, lower_limit):
        """
        Sets the physical limits (in calibrated units) of the selected output channel.

        Parameters
            Output index (int):    Sets the output to be used, where index could be any value from 1 to the number of available outputs
            Upper limit (float32): Defines the upper physical limit of the user output
            Lower limit (float32): Defines the lower physical limit of the user output
        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.LimitsSet', body_size=12)
        
        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        hex_rep += self.nanonisTCP.float32_to_hex(upper_limit)
        hex_rep += self.nanonisTCP.float32_to_hex(lower_limit)
        
        self.nanonisTCP.send_command(hex_rep)
        
        self.nanonisTCP.receive_response(0)
        
    def LimitsGet(self, output_index):
        """
        Returns the physical limits (in calibrated units) of the selected output channel.

        Parameters
            Output index (int) : Sets the output to be used, where index could be any value from 1 to the number of available outputs

        Returns
            Upper limit (float32): Defines the upper physical limit of the user output
            Lower limit (float32): Defines the lower physical limit of the user output

        """
        ## Make Header
        hex_rep = self.nanonisTCP.make_header('UserOut.LimitsGet', body_size=4)

        ## Arguments
        hex_rep += self.nanonisTCP.to_hex(output_index,4)
        
        self.nanonisTCP.send_command(hex_rep)
        
        response = self.nanonisTCP.receive_response()
        
        lower_limit = self.nanonisTCP.hex_to_float32(response[0:4])
        upper_limit = self.nanonisTCP.hex_to_float32(response[4:8])

        return [lower_limit, upper_limit]