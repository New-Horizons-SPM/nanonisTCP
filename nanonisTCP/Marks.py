# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 08:21:56 2022

@author: jced0001
"""

import numpy as np

class Marks:
    """
    Nanonis Marks In Scan Module
    """
    def __init__(self,NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def PointDraw(self,p,text,c=0):
        """
        Draws text at the specified point of the scan frame.
        This function can be very useful to mark an important location in the
        scan image (i.e. the position where the Tip Shaper executed).

        Parameters
        ----------
        p    : (x,y) coordinate (m) of the centre of the text
        text : Text characters to draw
        c    : RGB text colour (uint32)

        """
        text_size =  int(len(self.NanonisTCP.string_to_hex(text))/2)
        
        body_size = 16 + text_size
        
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Marks.PointDraw', body_size=body_size)
        
        hex_rep += self.NanonisTCP.float32_to_hex(p[0])
        hex_rep += self.NanonisTCP.float32_to_hex(p[1])
        hex_rep += self.NanonisTCP.to_hex(text_size,4)
        hex_rep += self.NanonisTCP.string_to_hex(text)
        hex_rep += self.NanonisTCP.to_hex(c,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)
        
    def LineDraw(self,start,end,c=0):
        """
        Draw a line in the scan frame

        Parameters
        ----------
        start : Start point (x,y) (m)
        end   : End point (x,y) (m)
        c     : Line colour (uint32)

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Marks.LineDraw', body_size=20)
        
        hex_rep += self.NanonisTCP.float32_to_hex(start[0])
        hex_rep += self.NanonisTCP.float32_to_hex(start[1])
        hex_rep += self.NanonisTCP.float32_to_hex(end[0])
        hex_rep += self.NanonisTCP.float32_to_hex(end[1])
        hex_rep += self.NanonisTCP.to_hex(c,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)
        
    def PointsErase(self,point_index=-1):
        """
        Erase the point specified by the index parameter from the scan frame.
        -1 erases all points

        Parameters
        ----------
        point_index : sets the index of the point to erase. The index is 
        comprised between 0 and the total number of drawn points minus one. To 
        see which point has which index, use the Marks.PointsGet function. 
        Value -1 erases all points.

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Marks.PointsErase', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(point_index,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)
        
    def LinesErase(self,point_index=-1):
        """
        Erase the line specified by the index parameter from the scan frame.
        -1 erases all lines

        Parameters
        ----------
        point_index : sets the index of the line to erase. The index is 
        comprised between 0 and the total number of drawn lines minus one. 
        To see which line has which index, use the Marks.LinesGet function.
        Value -1 erases all lines.

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Marks.LinesErase', body_size=4)
        
        hex_rep += self.NanonisTCP.to_hex(point_index,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response (check errors)
        self.NanonisTCP.receive_response(0)
        