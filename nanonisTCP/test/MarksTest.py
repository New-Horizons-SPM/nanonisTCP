# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 08:35:45 2022

@author: jced0001
"""
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!WARNING: RUNNING run_test() WILL CHANGE SETTINGS IN NANONIS. RUN IT ON A SIM!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

from nanonisTCP import nanonisTCP
from nanonisTCP.Marks import Marks
import traceback

def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501, debug=False, version=13520):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT, version=version)                        # Nanonis TCP interface
    try:
        marks = Marks(NTCP)                                                     # Nanonis TCP Marks In Scan Module
        
        """
        PointDraw
        """
        marks.PointDraw(p=(0,0),text="(0,0)",c=0)
        marks.PointDraw(p=(300e-9,-300e-9),text="(300nm,-300nm)",c=0)
        if(debug):
            print('Placed blacl text: "Xx." at (0,0)')
            print("----------------------------------------------------------------------")
        
        """
        LineDraw
        """
        start = (0,0)
        end   = (300e-9,-300e-9)
        marks.LineDraw(start=start, end=end)
        
        """
        PointsErase
        """
        marks.PointsErase()
        
        """
        LinesErase
        """
        marks.LinesErase()
    except:
        NTCP.close_connection()
        return traceback.format_exc()
        
    NTCP.close_connection()
    return "success"