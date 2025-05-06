# -*- coding: utf-8 -*-
"""
Created on Sat Apr 7 15:39:58 2025

@author: jced0001
"""

from nanonisTCP import nanonisTCP
from nanonisTCP.Util import Util
import traceback

"""
Set up the TCP connection and interface
"""
def run_test(TCP_IP='127.0.0.1', TCP_PORT=6501, debug=True, version=13520):
    # Listening Port: see Nanonis File>Settings>TCP Programming Interface
    NTCP = nanonisTCP(TCP_IP, TCP_PORT, version=version)                                # Nanonis TCP interface
    try:

        """
        Session Path Set/Get
        """
        util = Util(NTCP)                                                               # Nanonis Util Module

        util.SessionPathSet("C:/Users")                                                 # Set the session path
        session_path = util.SessionPathGet()                                            # Get the current session path
        if(debug):
            print("Session path")
            print(session_path)
            print("----------------------------------------------------------------------")
    except:
        NTCP.close_connection()
        print(traceback.format_exc())
        return(traceback.format_exc())
    
    NTCP.close_connection()
    return "success"