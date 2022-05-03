# -*- coding: utf-8 -*-
"""
Created on Mon May  2 15:32:25 2022

@author: jced0001
"""

class ZController:
    """
    Nanonis BZ-Controller Module
    """
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def ZPosSet(self,zpos):
        """
        Sets the Z position of the tip

        Parameters
        ----------
        zpos : Z position (m)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.ZPosSet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(zpos)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def ZPosGet(self):
        """
        Returns the current Z position of the tip

        Returns
        -------
        zpos : the current z position of the tip

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.ZPosGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        zpos = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return zpos
    
    def OnOffSet(self,on):
        """
        Switches the Z-Controller On or Off

        Parameters
        ----------
        on : True:  turn controller on
             False: turn controller off

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.OnOffSet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(on,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def OnOffGet(self):
        """
        Returns the status of the Z-Controller
        
        Returns
        -------
        z_status : indicates if the controller is on or off
                   True:  Z-Controller is on
                   False: Z-Controller is off
                   
        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.OnOffGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        z_status = self.NanonisTCP.hex_to_uint32(response[0:4])
        
        return z_status
    
    def SetpntSet(self,setpoint):
        """
        Sets the stpoint of the Z-Controller

        Parameters
        ----------
        setpoint : setpoint of the z-controller (A)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.SetpntSet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(setpoint)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def SetpntGet(self):
        """
        Returns the setpoint current of the Z-Controller

        Returns
        -------
        setpoint : setpoint current of the z-controller (A)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.SetpntGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        setpoint = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return setpoint
    
    def GainSet(self,p_gain,time_constant):
        """
        Sets the Z-Controller gains (P,I) and time settings

        Parameters
        ----------
        p_gain        : proportional gain of the regulation loop
        time_constant : time constant of the regulation loop
        i_gain        : integral gain of the regulation loop (I=P/T) (not used)

        """
        i_gain = p_gain/time_constant
        
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.GainSet', body_size=12)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(p_gain)
        hex_rep += self.NanonisTCP.float32_to_hex(time_constant)
        hex_rep += self.NanonisTCP.float32_to_hex(i_gain)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def GainGet(self):
        """
        Returns the Z-Controller gains (P,I) and time constant

        Returns
        -------
        None.

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.GainGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        p_gain        = self.NanonisTCP.hex_to_float32(response[0:4])
        time_constant = self.NanonisTCP.hex_to_float32(response[4:8])
        i_gain        = self.NanonisTCP.hex_to_float32(response[8:12])
        
        return [p_gain,time_constant,i_gain]
    
    def SwitchOffDelaySet(self,delay):
        """
        Sets the switch off delay in seconds of the Z-Controller

        Parameters
        ----------
        delay : Z-Controller switch off delay time (s)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.SwitchOffDelaySet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(delay)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def SwitchOffDelayGet(self):
        """
        Returns the switch off delay in seconds of the Z-Controller

        Returns
        -------
        delay : Z-Controller switch off delay time (s)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.SwitchOffDelayGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        delay = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return delay
    
    def TipLiftSet(self,tip_lift):
        """
        Sets the TipLift of the Z-Controller

        Parameters
        ----------
        tip_lift : tip lift (m)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.TipLiftSet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(tip_lift)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def TipLiftGet(self):
        """
        Returns the TipLift of the Z-Controller

        Returns
        -------
        tip_lift : tip lift (m)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.TipLiftGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        tip_lift = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return tip_lift
    
    def Home(self):
        """
        Moves the tip to its home position.
        
        This function moves the tip to the home position defined by the
        Home Absolute (m)/Home Relative (m) value. (Absolute and relative can 
        be switched in the controller configuration panel in the software or
        ZCtrl.HomePropsSet)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.Home', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response (check errors)
        self.NanonisTCP.receive_response(0)
    
    def HomePropsSet(self,rel_abs,home_pos):
        """
        Sets the current status of the Z-Controller Home switch and its 
        corresponding position

        Parameters
        ----------
        rel_abs  : relative or absolute.
                   0: no change (leave setting as is)
                   1: home position is absolute
                   2: home is relative to the current position
        home_pos : the home position value (m)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.HomePropsSet', body_size=6)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(rel_abs,2)
        hex_rep += self.NanonisTCP.float32_to_hex(home_pos)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response (check errors)
        self.NanonisTCP.receive_response(0)
    
    def HomePropsGet(self):
        """
        Returns the current status of the Z-Controller

        Returns
        -------
        rel_abs  : relative or absolute mode
                   False: home position is absolute
                   True:  home position is relative to current position
        home_pos : home position value (m)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.HomePropsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(6)
        
        rel_abs  = self.NanonisTCP.hex_to_uint16(response[0:2])
        home_pos = self.NanonisTCP.hex_to_float32(response[2:6])
        
        return [rel_abs,home_pos]
    
    def ActiveCtrlSet(self,index):
        """
        Sets the active Z-Controller

        Parameters
        ----------
        index : the index out of the list of controllers which can be retrieved
                by ZCtrl.ControllersListGet

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.ActiveCtrlSet', body_size=8)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(index,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response (check errors)
        self.NanonisTCP.receive_response(0)
        
    def CtrlListGet(self):
        """
        Returns the list of Z-Controllers and the index of the active 
        controller

        Returns
        -------
        controllers             : list of available Z-Controllers
        active_controller_index : index of the active Z-Controller

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.CtrlListGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        # list_of_controllers_size = self.NanonisTCP.hex_to_int16(response[0:4]) # Not needed
        number_of_controllers = self.NanonisTCP.hex_to_int16(response[4:8])
        
        if(not number_of_controllers): return [[],-1]                           # Return an empty list and -1 for the index if there are no available controllers
        
        idx = 8
        controllers = []
        for i in range(number_of_controllers):
            size = self.NanonisTCP.hex_to_int16(response[idx:idx+4])
            idx += 4
            controllers.append(response[idx:idx+size].decode())
            idx += size
        
        active_controller_index = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        
        return [controllers,active_controller_index]
    
    def Withdraw(self, wait_until_finished, timeout=-1):
        """
        Withdraws the tip

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.Withdraw', body_size=8)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(wait_until_finished,4)
        hex_rep += self.NanonisTCP.to_hex(timeout,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response (check errors)
        self.NanonisTCP.receive_response(0)
    
    def WithdrawRateSet(self,slew_rate):
        """
        Sets the Z-Controller withdraw slew rate

        Parameters
        ----------
        slew_rate : withdraw slew rate (m/s)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.WithdrawRateSet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(slew_rate)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response (check errors)
        self.NanonisTCP.receive_response(0)
    
    def WithdrawRateGet(self):
        """
        Returns the withdraw slew rate in m/s

        Returns
        -------
        slew_rate : withdraw slew rate (m/s)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.WithdrawRateGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        slew_rate  = self.NanonisTCP.hex_to_float32(response[0:4])
        
        return slew_rate
    
    def LimitsEnabledSet(self,limit_z_status):
        """
        Enables or disables the Z position limits

        Parameters
        ----------
        limit_z_status : enables/disables the Z limits
                         True:  Z limits enabled
                         False: Z limits disabled

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.LimitsEnabledSet', body_size=4)
        
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(limit_z_status,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response (check errors)
        self.NanonisTCP.receive_response(0)
    
    def LimitsEnabledGet(self):
        """
        Returns if the Z limits are enabled or disabled

        Returns
        -------
        limit_z_status : enables/disables the Z limits
                         True:  Z limits enabled
                         False: Z limits disabled

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.LimitsEnabledGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(4)
        
        limit_z_status = self.NanonisTCP.hex_to_int32(response[0:4])
        
        return limit_z_status
    
    def LimitsSet(self,z_high_limit,z_low_limit):
        """
        Sets the Z position high and low limits in meters.
        
        When the Z position limits are not enabled, this function has no effect

        Parameters
        ----------
        z_high_limit : high limit (m)
        z_low_limit  : low limit (m)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.LimitsSet', body_size=8)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(z_high_limit)
        hex_rep += self.NanonisTCP.float32_to_hex(z_low_limit)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive response (check errors)
        self.NanonisTCP.receive_response(0)
    
    def LimitsGet(self):
        """
        Returns the Z position high and low limits in meters.
        
        When the Z position limits are not enabled, they correspond to the 
        piezo range limits.

        Returns
        -------
        z_high_limit : high limit (m) (if not enabled, then piezo high limit)
        z_low_limit  : low limit (m) (if not enabled, then piezo low limit)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.LimitsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(8)
        
        z_high_limit = self.NanonisTCP.hex_to_float32(response[0:4])
        z_low_limit  = self.NanonisTCP.hex_to_float32(response[4:8])
        
        return [z_high_limit,z_low_limit]
    
    def StatusGet(self):
        """
        Returns the current status of the Z-Controller module

        Returns
        -------
        z_controller_status : returns if the controller is:
                              1: Off
                              2: On
                              3: Hold
                              4: Switching Off
                              5: Safe tip event occurred
                              6: Tip is currently withdrawing
        status_string       : String corresponding to the status
        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('ZCtrl.StatusGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(2)
        
        z_controller_status = self.NanonisTCP.hex_to_uint16(response[0:2])
        
        status_string = ["Off","On","Hold","Switching Off","Safe Tip Event","Withdrawing"][z_controller_status-1]
        
        return [z_controller_status,status_string]
        