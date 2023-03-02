# -*- coding: utf-8 -*-
"""
Created on Wed May  4 13:52:22 2022

@author: ben

Updated by
@author Julian Ceddia 3/3/22
"""

class TipShaper:
    """
    Nanonis Tip Shaper Module
    """
    def __init__(self,NanonisTCP):
        self.NanonisTCP = NanonisTCP
        
    def Start(self,wait_until_finished,timeout):
        """
        Starts the tip shaper procedure.

        Parameters
        ----------
        wait_until_finished : defines if this function waits until Tip Shaper
                              procedure stops.
                              0 = False (does not wait)
                              1 = True (waits)
                              
        timeout             : sets the number of milliseconds to wait if 
                            wait_until_finished is set to True. A value of -1 
                            means waiting forever [ms]. 
        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('TipShaper.Start', body_size=8)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(wait_until_finished,4)
        hex_rep += self.NanonisTCP.to_hex(timeout,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def PropsSet(self,Switch_off_delay="-default",Change_bias="-default", Bias="-default", Tip_lift="-default", Lift_time_1="-default",
                 Bias_lift="-default", Bias_settling_time="-default", Lift_height="-default", Lift_time_2="-default", 
                 End_wait_time="-default", Restore_feedback="-default"):
        """
        Sets the configuration of the tip shaper procedure. All inputs are 
        optional... -default will leave the setting as is in Nanonis

        Parameters
        ----------
        Switch_off_delay    : the time during which the Z position is averaged before
                            switching the Z controller off.
                            
        Change_bias         : decides whether the Bias value is applied right
                            before first Z ramping.
                            0 = no change
                            1 = True
                            2 = False
                            
        Bias                : is the value applied to the Bias signal if 
                            Change_bias is True [V]. 
                            
        Tip_lift            : defines the relative height the tip is going to ramp
                            for the first time (from current Z position) [m].
                            
        Lift_time_1         : defines the time to ramp Z from current Z position
                            by the Tip_lift amount [s]. 
                            
        Bias_lift           : the Bias voltage applied just after the first Z
                            ramping [V]. 
                            
        Bias_settling_time  : the time to wait after applying the Bias Lift value,
                            and it is also the time to wait after applying Bias
                            before ramping Z for the first time [s]. 
                            
        Lift_height         : returns the height the tip is going to ramp for the
                            second time [m]. 
                            
        Lift_time_2         : given time to ramp Z in the second ramping [s].
                            
        End_wait_time       : time to wait after restoring the initial Bias voltage
                            (just after finishing second ramping) [s].
                            
        Restore_feedback    : returns whether the initial Z-controller status is
                            restored at the end of the tip shaper procedure.
                            0 = False
                            1 = True

        """
        default_args = self.PropsGet()                                          # Store all the current tip shaping settings in nanonis
        
        # Order matters here
        tipShaperArgs = [Switch_off_delay]
        tipShaperArgs.append(Change_bias)
        tipShaperArgs.append(Bias)
        tipShaperArgs.append(Tip_lift)
        tipShaperArgs.append(Lift_time_1)
        tipShaperArgs.append(Bias_lift)
        tipShaperArgs.append(Bias_settling_time)
        tipShaperArgs.append(Lift_height)
        tipShaperArgs.append(Lift_time_2)
        tipShaperArgs.append(End_wait_time)
        tipShaperArgs.append(Restore_feedback)
        
        for i,a in enumerate(tipShaperArgs):
            if(a=="-default"):
                tipShaperArgs[i] = default_args[i]
                
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('TipShaper.PropsSet', body_size=44)
        
        ## Arguments 
        hex_rep += self.NanonisTCP.float32_to_hex(tipShaperArgs[0])
        hex_rep += self.NanonisTCP.to_hex(tipShaperArgs[1],4)
        hex_rep += self.NanonisTCP.float32_to_hex(tipShaperArgs[2])
        hex_rep += self.NanonisTCP.float32_to_hex(tipShaperArgs[3])
        hex_rep += self.NanonisTCP.float32_to_hex(tipShaperArgs[4])
        hex_rep += self.NanonisTCP.float32_to_hex(tipShaperArgs[5])
        hex_rep += self.NanonisTCP.float32_to_hex(tipShaperArgs[6])
        hex_rep += self.NanonisTCP.float32_to_hex(tipShaperArgs[7])
        hex_rep += self.NanonisTCP.float32_to_hex(tipShaperArgs[8])
        hex_rep += self.NanonisTCP.float32_to_hex(tipShaperArgs[9])
        hex_rep += self.NanonisTCP.to_hex(tipShaperArgs[10],4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def PropsGet(self):
        """
        Returns the configuration of the tip shaper procedure.

        Returns
        -------
        Switch_off_delay    : the time during which the Z position is averaged before
                            switching the Z controller off.
                            
        Change_bias         : decides whether the Bias value is applied right
                            before first Z ramping.
                            0 = no change
                            1 = True
                            2 = False
                            
        Bias                : is the value applied to the Bias signal if 
                            Change_bias is True [V]. 
                            
        Tip_lift            : defines the relative height the tip is going to ramp
                            for the first time (from current Z position) [m].
                            
        Lift_time_1         : defines the time to ramp Z from current Z position
                            by the Tip_lift amount [s]. 
                            
        Bias_lift           : the Bias voltage applied just after the first Z
                            ramping [V]. 
                            
        Bias_settling_time  : the time to wait after applying the Bias Lift value,
                            and it is also the time to wait after applying Bias
                            before ramping Z for the first time [s]. 
                            
        Lift_height         : returns the height the tip is going to ramp for the
                            second time [m]. 
                            
        Lift_time_2         : given time to ramp Z in the second ramping [s].
                            
        End_wait_time       : time to wait after restoring the initial Bias voltage
                            (just after finishing second ramping) [s].
                            
        Restore_feedback    : returns whether the initial Z-controller status is
                            restored at the end of the tip shaper procedure.
                            0 = False
                            1 = True

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('TipShaper.PropsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(44)
        
        Switch_off_delay    = self.NanonisTCP.hex_to_float32(response[0:4])
        Change_bias         = self.NanonisTCP.hex_to_uint32(response[4:8])
        Bias                = self.NanonisTCP.hex_to_float32(response[8:12])
        Tip_lift            = self.NanonisTCP.hex_to_float32(response[12:16])
        Lift_time_1         = self.NanonisTCP.hex_to_float32(response[16:20])
        Bias_lift           = self.NanonisTCP.hex_to_float32(response[20:24])
        Bias_settling_time  = self.NanonisTCP.hex_to_float32(response[24:28])
        Lift_height         = self.NanonisTCP.hex_to_float32(response[28:32])
        Lift_time_2         = self.NanonisTCP.hex_to_float32(response[32:36])
        End_wait_time       = self.NanonisTCP.hex_to_float32(response[36:40])
        Restore_feedback    = self.NanonisTCP.hex_to_uint32(response[40:44])
        
        return [Switch_off_delay,Change_bias,Bias,Tip_lift,Lift_time_1,Bias_lift,
                Bias_settling_time,Lift_height,Lift_time_2,End_wait_time,
                Restore_feedback]