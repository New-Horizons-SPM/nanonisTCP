# -*- coding: utf-8 -*-
"""
Created on Mon May  2 15:36:03 2022

@author: jced0001
"""

import time
from nanonisTCP import nanonisTCP
from nanonisTCP.ZController import ZController

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6502, make_plot=False):
    
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT)                                         # Nanonis TCP interface
    
    zctrl = ZController(NTCP)                                                   # Nanonis Z-Controller Module
    
    try:
        """
        ZPos Set/Get
        """
        zctrl.ZPosSet(140e-9)
        zpos = zctrl.ZPosGet()
        print("Z-Controller ZPos")
        print("zpos: " + str(zpos) + " m")
        print("----------------------------------------------------------------------")
        
        """
        OnOff Set/Get
        """
        zctrl.OnOffSet(on=False)
        time.sleep(1)                                                           # Need to sleep otherwise it doesn't update in time
        z_status = zctrl.OnOffGet()
        print("Z-Controller Status")
        print("Controller: " + ["Off","On"][z_status])
        print("----------------------------------------------------------------------")
        
        """
        Setpnt Set/Get
        """
        zctrl.SetpntSet(27e-12)
        setpoint = zctrl.SetpntGet()
        print("Z-Controller Setpoint")
        print("Setpoint: " + str(setpoint) + " A")
        print("----------------------------------------------------------------------")
        
        """
        Gain Set/Get
        """
        zctrl.GainSet(3e-12, 155e-6)
        p_gain,time_constant,i_gain = zctrl.GainGet()
        print("Z-Controller Gain")
        print("proportional gain: " + str(p_gain))
        print("integral gain:     " + str(i_gain))
        print("time constant:     " + str(time_constant))
        print("----------------------------------------------------------------------")
        
        """
        Switch off delay Set/Get
        """
        zctrl.SwitchOffDelaySet(0.07575)
        delay = zctrl.SwitchOffDelayGet()
        print("Z-Controller Switch Off Delay")
        print("Switch off delay: " + str(delay) + " s")
        print("----------------------------------------------------------------------")
        
        """
        Tip Lift Set/Get
        """
        zctrl.TipLiftSet(19e-9)
        tip_lift = zctrl.TipLiftGet()
        print("Z-Controller Tip Lift")
        print("Tip Lift: " + str(tip_lift) + " m")
        print("----------------------------------------------------------------------")
        
        """
        Home Properties Set/Get
        """
        zctrl.HomePropsSet(1, 160e-9)
        abs_rel,home_pos = zctrl.HomePropsGet()
        print("Z-Controller Home Properties")
        print("Mode:     " + ["Absolute","Relative"][abs_rel])
        print("Home Pos: " + str(home_pos) + " m")
        print("----------------------------------------------------------------------")
        
        """
        Home
        """
        zctrl.Home()
        
        """
        Control List Get
        """
        controllers,active_controller = zctrl.CtrlListGet()
        print("Z-Controller Controller")
        print("Available Controllers: " + str(controllers))
        print("Active Controller:     " + controllers[active_controller])
        print("----------------------------------------------------------------------")
        
        """
        Withdraw Rate Set/Get
        """
        zctrl.WithdrawRateSet(20e-9)
        slew_rate = zctrl.WithdrawRateGet()
        print("Z-Controller Slew Rate")
        print("Slew Rate: " + str(slew_rate) + " m/s")
        print("----------------------------------------------------------------------")
        
        """
        Withdraw
        """
        time.sleep(0.5)
        zctrl.Withdraw(wait_until_finished=True)
        
        """
        Limits Enabled Set
        """
        zctrl.LimitsEnabledSet(limit_z_status=True)
        limit_z_status = zctrl.LimitsEnabledGet()
        print("Z-Controller Z Limits Enabled/Disabled")
        print("Z limits " + ["disabled","enabled"][limit_z_status])
        print("----------------------------------------------------------------------")
        
        """
        Limits Set/Get
        """
        zctrl.LimitsSet(200e-9, -210e-9)
        z_high_limit, z_low_limit = zctrl.LimitsGet()
        print("Z-Controller Z Limits")
        print("Z high limit: " + str(z_high_limit) + " m")
        print("Z low limit:  " + str(z_low_limit) + " m")
        print("----------------------------------------------------------------------")
        
        """
        Z Controller Status
        """
        _,status_string = zctrl.StatusGet()
        print("Z-Controller Status")
        print("Controller status: " + status_string)
        print("----------------------------------------------------------------------")
        
    except Exception as e:
        print(e)
    
    NTCP.close_connection()