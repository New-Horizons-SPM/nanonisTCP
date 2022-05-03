# -*- coding: utf-8 -*-
"""
Created on Tue May  3 19:26:25 2022

@author: Julian
"""

class Motor:
    """
    Nanonis Coarse Motion (Motor) Module
    """
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def StartMove(self,direction,steps,wait_until_finished=True,group=0):
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
                              0: Group 1
                              1: Group 2
                              2: Group 3
                              3: Group 4
                              5: Group 6

        """
        direction_dict = { "X+" : 0,
                           "X-" : 1,
                           "Y+" : 2,
                           "Y-" : 3,
                           "Z+" : 4,
                           "Z-" : 5,
                           }
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Motor.StartMove', body_size=14)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(direction_dict[direction],4)
        hex_rep += self.NanonisTCP.to_hex(steps,2)
        hex_rep += self.NanonisTCP.to_hex(group,4)
        hex_rep += self.NanonisTCP.to_hex(wait_until_finished,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)