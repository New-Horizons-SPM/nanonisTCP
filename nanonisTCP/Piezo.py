# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 22:51:52 2022

@author: jced0001
"""

class Piezo:
    """
    Nanonis Piezo Module
    """
    def __init__(self,NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def TiltSet(self,tilt_x=None,tilt_y=None):
        """
        Configures the tilt correction parameters. Passing in None for either x
        or y tilt keeps the setting as is in nanonis.

        Parameters
        ----------
        tilt_x : Sets by which angle to correct the tilt in the X direction
        tilt_y : Sets by which angle to correct the tilt in the Y direction

        """
        n_tilt_x,n_tilt_y = self.TiltGet()
        if(not tilt_x): tilt_x = n_tilt_x
        if(not tilt_y): tilt_y = n_tilt_y
        
        hex_rep = self.NanonisTCP.make_header('Piezo.TiltSet', body_size=8)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(tilt_x)
        hex_rep += self.NanonisTCP.float32_to_hex(tilt_y)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def TiltGet(self):
        """
        Returns the tilt correction parameters.

        Returns
        -------
        tilt_x : Sets by which angle to correct the tilt in the X direction
        tilt_y : Sets by which angle to correct the tilt in the Y direction

        """
        hex_rep = self.NanonisTCP.make_header('Piezo.TiltGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(8)
        
        tilt_x = self.NanonisTCP.hex_to_float32(response[0:4])
        tilt_y = self.NanonisTCP.hex_to_float32(response[4:8])
        
        return [tilt_x,tilt_y]
    
    def RangeSet(self,range_x=None,range_y=None,range_z=None):
        """
        Sets the piezo range (m) values for all 3 aces (X,Y,Z). Leave param as 
        None means it will remain as is in nanonis.

        Parameters
        ----------
        range_x : range of the X piezo (m)
        range_y : range of the Y piezo (m)
        range_z : range of the Z piezo (m)

        """
        n_range_x,n_range_y,n_range_z = self.RangeGet()
        if(not range_x): range_x = n_range_x
        if(not range_y): range_y = n_range_y
        if(not range_z): range_z = n_range_z
    
        hex_rep = self.NanonisTCP.make_header('Piezo.RangeSet', body_size=12)
        
        ## Arguments
        hex_rep += self.NanonisTCP.float32_to_hex(range_x)
        hex_rep += self.NanonisTCP.float32_to_hex(range_y)
        hex_rep += self.NanonisTCP.float32_to_hex(range_z)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def RangeGet(self):
        """
        Returns the piezo range (m) for all 3 axes (X,Y,Z)

        Returns
        -------
        range_x : range of the X piezo (m)
        range_y : range of the Y piezo (m)
        range_z : range of the Z piezo (m)

        """
        hex_rep = self.NanonisTCP.make_header('Piezo.RangeGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(12)
        
        range_x = self.NanonisTCP.hex_to_float32(response[0:4])
        range_y = self.NanonisTCP.hex_to_float32(response[4:8])
        range_z = self.NanonisTCP.hex_to_float32(response[8:12])
        
        return [range_x,range_y,range_z]
    
    def DriftCompGet(self):
        """
        Returns the drift compensation parameters

        Returns
        ----------
        on    : True: Turn compensation on
                False: Turn compensation off
        vx    : linear speed applied to the X piezo (m/s)
        vy    : linear speed applied to the Y piezo (m/s)
        vz    : linear speed applied to the Z piezo (m/s)
        xsat  : indicates if the X drift correction reached 10% of piezo range
        ysat  : indicates if the Y drift correction reached 10% of piezo range
        zsat  : indicates if the Z drift correction reached 10% of piezo range

        """
        hex_rep = self.NanonisTCP.make_header('Piezo.DriftCompGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response(28)
        
        status = self.NanonisTCP.hex_to_uint32(response[0:4])
        vx     = self.NanonisTCP.hex_to_float32(response[4:8])
        vy     = self.NanonisTCP.hex_to_float32(response[8:12])
        vz     = self.NanonisTCP.hex_to_float32(response[12:16])
        xsat   = self.NanonisTCP.hex_to_uint32(response[16:20])
        ysat   = self.NanonisTCP.hex_to_uint32(response[20:24])
        zsat   = self.NanonisTCP.hex_to_uint32(response[24:28])
        
        return [status,vx,vy,vz,xsat,ysat,zsat]
        
    def DriftCompSet(self,on,vx=[],vy=[],vz=[]):
        """
        Configures the drift compensation parameters

        Parameters
        ----------
        on : True: Turn compensation on
             False: Turn compensation off
        vx : linear speed applied to the X piezo (m/s)
        vy : linear speed applied to the Y piezo (m/s)
        vz : linear speed applied to the Z piezo (m/s)

        """
        _,n_vx,n_vy,n_vz,_,_,_ = self.DriftCompGet()
        if(not len(vx)): vx = n_vx
        if(not len(vy)): vy = n_vy
        if(not len(vz)): vz = n_vz
    
        hex_rep = self.NanonisTCP.make_header('Piezo.DriftCompSet', body_size=16)
        ## Arguments
        hex_rep += self.NanonisTCP.to_hex(on,4)
        hex_rep += self.NanonisTCP.float32_to_hex(vx)
        hex_rep += self.NanonisTCP.float32_to_hex(vy)
        hex_rep += self.NanonisTCP.float32_to_hex(vz)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
        