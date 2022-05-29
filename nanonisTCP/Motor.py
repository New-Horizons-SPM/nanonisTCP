# -*- coding: utf-8 -*-
"""
Created on Tue May  3 19:26:25 2022

@author: Julian Ceddia
"""

class Motor:
    """
    Nanonis Coarse Motion (Motor) Module
    """
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def StartMove(self,direction,steps,wait_until_finished=True,group=1):
        """
        Moves the coarse positioning device (motor, piezo actuator...)

        Parameters
        ----------
        direction : selects in which direction to move. Note that depending on 
                    your motor controller and setuo only the Z axis or Z- axis
                    may work
                    Possible values: "X+","X-","Y+","Y-","Z+","Z-"
        steps     : number of motor steps to move in the specified direction
        wait_until_finished : defines if this function only returns when the
                              motor reaches its destination or the movement
                              stops
                              False: Return immediately
                              True:  Return once function has reached its 
                                     destination
        group               : is the selection of groups defined in the motor
                              control module. If the motor doesn't support the
                              selection of groups, set it to 0
                              1: Group 1
                              2: Group 2
                              3: Group 3
                              4: Group 4
                              5: Group 5
                              6: Group 6

        """
        direction_dict = { "X+" : 0,
                           "X-" : 1,
                           "Y+" : 2,
                           "Y-" : 3,
                           "Z+" : 4,
                           "Z-" : 5,
                           }
        group -= 1                                                              # Make this more sensible
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Motor.StartMove', body_size=14)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(direction_dict[direction],4)
        hex_rep += self.NanonisTCP.to_hex(steps,2)
        hex_rep += self.NanonisTCP.to_hex(group,4)
        hex_rep += self.NanonisTCP.to_hex(wait_until_finished,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def StartClosedLoop(self,abs_rel,target_x,target_y,target_z,wait_until_finished):
        """
        Moves the coarse positioning device (motor, piezo actuator...) in 
        closed loop. This is not supported by all motor control modules

        Parameters
        ----------
        abs_rel             : selects if moving in relative or absolute mode
                              False: relative
                              True:  absolute
        target_x            : target position to move in x (m)
        target_y            : target position to move in y (m)
        target_z            : target position to move in z (m)
        wait_until_finished : defines if this function returns immediately or
                              after reaching destination
                              False: Return immediately
                              True:  Wait until position is reached before 
                                     returning

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Motor.StartClosedLoop', body_size=32)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(abs_rel,4)
        hex_rep += self.NanonisTCP.float64_to_hex(target_x)
        hex_rep += self.NanonisTCP.float64_to_hex(target_y)
        hex_rep += self.NanonisTCP.float64_to_hex(target_z)
        hex_rep += self.NanonisTCP.to_hex(wait_until_finished,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def StopMove(self):
        """
        Stops the motor motion

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Motor.StopMove', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def PosGet(self):
        """
        Returns the positions of the motor control module.

        Returns
        -------
        x_pos : the x position (m)
        y_pos : the y position (m)
        z_pos : the z position (m)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Motor.PosGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(24)
        
        x_pos = self.NanonisTCP.hex_to_float64(response[0:8])
        y_pos = self.NanonisTCP.hex_to_float64(response[8:16])
        z_pos = self.NanonisTCP.hex_to_float64(response[16:24])
        
        return [x_pos,y_pos,z_pos]
    
    def StepCounterGet(self,reset_x=False,reset_y=False,reset_z=False):
        """
        Retuns the step counter values of X, Y, Z.
        
        This function also allows to reset the step counters after reading 
        their values through inputs reset_x,reset_y,reset_z

        Parameters
        ----------
        reset_x : reset the x counter (True: reset, False: don't reset)
        reset_y : reset the y counter (True: reset, False: don't reset)
        reset_z : reset the z counter (True: reset, False: don't reset)

        Returns
        -------
        counter_x : x step counter value
        counter_y : y step counter value
        counter_z : z step counter value

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Motor.StepCounterGet', body_size=12)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(reset_x,4)
        hex_rep += self.NanonisTCP.to_hex(reset_y,4)
        hex_rep += self.NanonisTCP.to_hex(reset_z,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(12)
        
        counter_x = self.NanonisTCP.hex_to_int32(response[0:4])
        counter_y = self.NanonisTCP.hex_to_int32(response[4:8])
        counter_z = self.NanonisTCP.hex_to_int32(response[8:12])
        
        return [counter_x,counter_y,counter_z]
    
    def FreqAmpGet(self):
        """
        Returns the frequency (Hz) and amplitude (V) of the motor control 
        module.
        
        This function is only available for PD5, PMD4, and Attocube ANC150
        devices.


        Returns
        -------
        frequency : frequency (Hz)
        amplitude : amplitude (V)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Motor.FreqAmpGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(8)
        
        frequency = self.NanonisTCP.hex_to_float32(response[0:4])
        amplitude = self.NanonisTCP.hex_to_float32(response[4:8])
        
        return [frequency,amplitude]
        
    def FreqAmpSet(self,frequency,amplitude,axis=0):
        """
        Sets the frequency (Hz) and amplitude (V) of the motor control

        Parameters
        ----------
        frequency : frequency (Hz)
        amplitude : amplitude (V)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Motor.FreqAmpSet', body_size=10)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(frequency)
        hex_rep += self.NanonisTCP.float32_to_hex(amplitude)
        hex_rep += self.NanonisTCP.to_hex(axis,2)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)