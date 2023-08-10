# -*- coding: utf-8 -*-
"""
Created on Wed Aug 9 17:15:00 2023

@author: Liam
"""

import numpy as np

class Pattern:
    """
    Nanonis Pattern Module
    """
    def __init__(self,NanonisTCP):
        self.NanonisTCP = NanonisTCP
        
    def ExpOpen(self):
        """
        Opens the selected grid experiment.

        """
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Pattern.ExpOpen', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def ExpStart(self,pattern):
        """
        Starts the selected grid experiment.

        Before using this function, select the experiment through Pattern.PropsSet, 
        and be sure to have it open in the software or through the function 
        Pattern.ExpOpen. Otherwise it will give an error saying that the experiment 
        has not been configured yet.

        Parameters
        ----------
        pattern     : defines switches the active pattern to this value before 
                      starting the grid experiment. 
                        : 0 = no change
                        : 1 = Grid
                        : 2 = Line
                        : 3 = Cloud
                    

        Returns
        -------
        None.

        """
        # Create int assignments to allow string inputs
        pattern_dict = {
            'no change' : 0,
            'Grid'      : 1,
            'Line'      : 2,
            'Cloud'     : 3
        }

        # Make sure input is one of the strings or int assignments
        if pattern not in pattern_dict.keys() and pattern not in pattern_dict.values():
            raise Exception('pattern input must be either:\n0 = no change \n1 = Grid\n2 = Line\n3 = Cloud')
        # Convert string to int assignment
        if type(pattern) is str: pattern = pattern_dict[pattern]

        body_size = 2                                                       # 2 bytes for pattern (uint16)
        
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Pattern.ExpStart', body_size=body_size)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(pattern,2)
        
        self.NanonisTCP.send_command(hex_rep)
        
        # Receive Response
        self.NanonisTCP.receive_response(0)

    def ExpPause(self, pause):
        """
        Pauses or resumes the selected grid experiment.

        Parameters
        ----------
        pause:   : 0 = Resume
                 : 1 = Pause

        Issues
        ------
        Cant pause on the same socket that the experiment was started from.
        If you want to pause or stop, open a new TCP connection under a different port 
        or disconnect and reconnect with the current port.

        """

        pause_dict = {
            'resume': 0,
            'pause' : 1
        }

        if type(pause) is str: pause = pause_dict[pause]

        body_size = 4                                                       # 2 bytes for pause (uint32)
        
        ## Make Header
        hex_rep = self.NanonisTCP.make_header('Pattern.ExpPause', body_size=body_size)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(pause,4)

        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)

    
    def ExpStop(self):
        """
        Stops the selected grid experiment.

        Issues
        ------
        Cant pause on the same socket that the experiment was started from.
        If you want to pause or stop, open a new TCP connection under a different port 
        or disconnect and reconnect with the current port.

        """

        hex_rep = self.NanonisTCP.make_header('Pattern.ExpStop', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
    
    def ExpStatusGet(self):
        """
        Returns the status of the selected grid experiment.
        
        Returns
        -------
        status : 0: Not running. 1: Running

        """
        hex_rep = self.NanonisTCP.make_header('Pattern.ExpStatusGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        status = self.NanonisTCP.hex_to_int32(response[0:4])
        
        return status
        
    def GridSet(self,num_points_x,num_points_y,x,y,w,h,angle):
        """
        Sets the grid size parameters.

        Parameters
        ----------
        num_points_x            : number of points in x that defines the grid
        num_points_y            : number of points in y that defines the grid
        x                       : x (m) coordinate of the centre of the grid 
        y                       : y (m) coordinate of the centre of the grid 
        w                       : the width (m) of the grid 
        h                       : the height (m) of the grid 
        angle                   : the rotation angle (deg) of the grid

        Returns
        -------
        None.

        Defaults
        --------
        set_active_pattern      : defines if the pattern switches to Grid, 
                                  in case it was not Cloud already.
                                    : 0 = Off 
                                    : 1 = On

                                  DEFAULT = 1

        grid_scan_frame         : defines if the grid size should be set like 
                                  the scan frame size. 
                                  : 0 = No 
                                  : 1 = Yes

                                DEFAULT = 0

        """
            
        body_size = 4 + 2*4 + 4 + 5*4                                    # 4 bytes for set_active_pattern (uint32), 2 x 4 bytes for num_points_x+y (int), 4 bytes for grid_scan_frame (uint32), 5 x 4 bytes for x, y, w, h, angle (float32)
        
        hex_rep = self.NanonisTCP.make_header('Pattern.GridSet', body_size=body_size)

        ## arguments

        set_active_pattern  = 1                                         # Useless, setting default to 1. Why call Grid set if not to activate the Grid?
        grid_scan_frame     = 0                                         # Useless, this function is helpful in the Nanonis GUI, but not in command line.

        hex_rep += self.NanonisTCP.to_hex(set_active_pattern,4)         
        hex_rep += self.NanonisTCP.to_hex(num_points_x,4)
        hex_rep += self.NanonisTCP.to_hex(num_points_y,4)
        hex_rep += self.NanonisTCP.to_hex(grid_scan_frame,4)            
        hex_rep += self.NanonisTCP.float32_to_hex(x)
        hex_rep += self.NanonisTCP.float32_to_hex(y)
        hex_rep += self.NanonisTCP.float32_to_hex(w)
        hex_rep += self.NanonisTCP.float32_to_hex(h)
        hex_rep += self.NanonisTCP.float32_to_hex(angle)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def GridGet(self):
        """
        Returns the grid size parameters.

        Returns
        -------
        num_points_x   : number of points in x that defines the grid
        num_points_y   : number of points in y that defines the grid
        x              : x (m) coordinate of the centre of the grid 
        y              : y (m) coordinate of the centre of the grid 
        w              : the width (m) of the grid 
        h              : the height (m) of the grid 
        angle          : the rotation angle (deg) of the grid


        """
        hex_rep = self.NanonisTCP.make_header('Pattern.GridGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        idx = 0
        args = []
        for i in range(2):                                              # Two int32 responses requiring 4 bytes each
            args.append(self.NanonisTCP.hex_to_int32(response[idx:idx+4]))
            idx += 4
        
        for i in range(5):                                              # Five float32 responses requiring 4 bytes each
            args.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
            idx += 4

        num_points_x, num_points_y, x, y, w, h, angle = args
        
        return [num_points_x, num_points_y, x, y, w, h, angle]
    
    def LineSet(self,num_points,x1,y1,x2,y2):
        """
        Sets the line size parameters.

        Parameters
        ----------
        num_points    : number of points that defines the line
        x1            : x (m) coordinate of the start of the line 
        y1            : y (m) coordinate of the start of the line 
        x2            : x (m) coordinate of the end of the line 
        y2            : y (m) coordinate of the end of the line 

        Returns
        -------
        None.

        Default Values
        --------------
        set_active_pattern      : defines if the pattern switches to Line, 
                                  in case it was not Line already.
                                    : 0 = Off 
                                    : 1 = On

                                  DEFAULT = 1

        line_scan_frame         : defines if the line size should be set like 
                                  the scan frame size. 
                                  : 0 = No 
                                  : 1 = Yes

                                DEFAULT = 0

        """
            
        body_size = 4 + 4 + 4 + 4*4                                    # 4 bytes for set_active_pattern (uint32), 4 bytes for num_points (int), 4 bytes for line_scan_frame (uint32), 4 x 4 bytes for x1, y1, x2, y2 (float32)
        
        hex_rep = self.NanonisTCP.make_header('Pattern.LineSet', body_size=body_size)

        ## arguments

        set_active_pattern  = 1                                            # Useless, setting default to 1. Why call Grid set if not to activate the Grid?
        line_scan_frame     = 0                                            # Useless, this function is helpful in the Nanonis GUI, but not in command line.

        hex_rep += self.NanonisTCP.to_hex(set_active_pattern,4)         
        hex_rep += self.NanonisTCP.to_hex(num_points,4)
        hex_rep += self.NanonisTCP.to_hex(line_scan_frame,4)            
        hex_rep += self.NanonisTCP.float32_to_hex(x1)
        hex_rep += self.NanonisTCP.float32_to_hex(y1)
        hex_rep += self.NanonisTCP.float32_to_hex(x2)
        hex_rep += self.NanonisTCP.float32_to_hex(y2)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)

    def LineGet(self):
        """
        Returns the line size parameters.

        Returns
        -------
        num_points     : number of points that defines the line
        x1             : x (m) coordinate of the start of the line 
        y1             : y (m) coordinate of the start of the line 
        x2             : x (m) coordinate of the end of the line 
        y2             : y (m) coordinate of the end of the line 


        """
        hex_rep = self.NanonisTCP.make_header('Pattern.LineGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        
        args = []
        args.append(self.NanonisTCP.hex_to_int32(response[0:4]))
        
        idx = 4
        for i in range(4):                                              # Four float32 responses requiring 4 bytes each
            args.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
            idx += 4

        num_points, x1, y1, x2, y2 = args
        
        return [num_points, x1, y1, x2, y2]

    def CloudSet(self,x,y):
        """
        Configures a cloud of points.

        Parameters
        ----------
        x   : x (m) is a 1D array of the x coordinates of the of the points defining the cloud
        y   : y (m) is a 1D array of the y coordinates of the of the points defining the cloud

        Returns
        -------
        None.


        Default Values
        --------------
        set_active_pattern      : defines if the pattern switches to Cloud, 
                                  in case it was not Cloud already.
                                  0 = Off, 1 = On
                                 
                                  DEFAULT = 1

        num_points              : number of points that defines the cloud, AND
                                  it defines the size of the 1D arrays for x
                                  and y coordinates
                                  
                                  DEFAULT = len(x)

        """

        if not type(x) is list: 
            raise Exception('x must be a 1D list')
        
        if not type(y) is list: 
            raise Exception('y must be a 1D list')

        if np.array(x).ndim != 1 or np.array(y).ndim != 1:
            raise Exception('x and y inputs must be separate 1D lists of ordinates')
        
        if len(x) != len(y):
            raise Exception('x and y inputs must have the same number of elements (x (%.0i), and y (%.0i))' % (len(x), len(y)))

        set_active_pattern=1                                                      # Useless, setting default to 1. Why call Cloud set if not to activate the Cloud?
        
        num_points=len(x)                                                         # Calculate num_points from length of input vector.
        
        body_size = 4 + 4 + num_points*(4 + 4)                                    # 4 bytes for set_active_pattern (uint32), 4 bytes for num_points (int), 2 * 4 * num_points bytes for the total number of elements in both x and y 1D arrays (float32)
        
        hex_rep = self.NanonisTCP.make_header('Pattern.CloudSet', body_size=body_size)

        ## arguments

        hex_rep += self.NanonisTCP.to_hex(set_active_pattern,4)         
        
        hex_rep += self.NanonisTCP.to_hex(num_points,4)

        for p in x:
            hex_rep += self.NanonisTCP.float32_to_hex(p)
        
        for p in y:
            hex_rep += self.NanonisTCP.float32_to_hex(p)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)

    def CloudGet(self):
        """
        Returns the cloud configuration.

        Returns
        -------
        num_points     : number of points that defines the cloud
        x              : x (m) coordinates of the cloud 
        y              : y (m) coordinates of the cloud

        """
        hex_rep = self.NanonisTCP.make_header('Pattern.CloudGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        
        num_points = self.NanonisTCP.hex_to_int32(response[0:4])
        
        idx = 4
        x = []
        for i in range(num_points):                                              # Four bytes for each point in x (float32)
            x.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
            idx += 4

        y = []
        for i in range(num_points):                                              # Four bytes for each point in y (float32)
            y.append(self.NanonisTCP.hex_to_float32(response[idx:idx+4]))
            idx += 4
        
        return [num_points, x, y]

        
    def PropsSet(self,exp_name,basename,premeasure_delay,ext_VI_path='/',save_scan_channels=1):
        """
        Sets the configuration of the Grid experiment section in the Scan module.

        Returns
        -------
        exp_name            : is the name of the selected experiment. 
                              Must be one of: (example)
                                : 'Bias Spectroscopy ASCII'
                                : 'Bias Spectroscopy BINARY'
                                : 'Bias Sweep'
                                : 'Generic Sweep'
                                : 'Z Spectroscopy ASCII'
                                : 'Z Spectroscopy BINARY'
                                : 'Approach-Retract'
                                : 'DIO Trigger'
                                : 'External VI...'
                              For a full list of experiment names, see Pattern.PropsGet()
        basename            : sets the basename of the experiment file
        premeasure_delay    : is the time (s) to wait on each point before 
                              performing the experiment 
        ext_VI_path         : sets the path of the external VI. Relevant only for
                              exp_name = 'External VI...'
        save_scan_channels  : sets if the scan channels are saved into the grid 
                              experiment file. 
                                : 0 = Off 
                                : 1 = On

        """

        exp_names = ['Bias Spectroscopy ASCII', 'Bias Spectroscopy BINARY', 'Bias Sweep', 'Generic Sweep', 'Z Spectroscopy ASCII', 'Z Spectroscopy BINARY', 'Approach-Retract', 'DIO Trigger', 'External VI...']

        if exp_name not in exp_names:
            raise Exception('Experiment name not valid. Check spelling and case (exact). Must be one of: ' + ', '.join(map(str,exp_names)))

        ###################
        #------NOTE-------#
        ###################
        # Choosing exp_name='External VI...' given weird result in Nanonis GUI
        # I think it is trying to find the name of the VI given the path,
        # but if the path is false it returns some hex code instead.
        # Need to test with appropriate external VI.
            # Also, basename will not update on the GUI but does actually affect the name of the saved files

        if exp_name == 'External VI...':
            print('Make sure you have passed the External VI path in PropsSet(ext_VI_path='')')

        body_size = 3*4 + int(len(self.NanonisTCP.string_to_hex(exp_name))/2) + int(len(self.NanonisTCP.string_to_hex(basename))/2) + int(len(self.NanonisTCP.string_to_hex(ext_VI_path))/2) + 4 + 4            # 4*3 bytes for each string length, 1 byte for each character in the strings (exp_name, basename, ext_VI_path), 4 bytes for pre-measure delay (float32), and 4 bytes for save_scan_channels (uint32).

        hex_rep = self.NanonisTCP.make_header('Pattern.PropsSet', body_size=body_size)
        
        ## arguments
        hex_rep += self.NanonisTCP.to_hex(len(exp_name),4)
        hex_rep += self.NanonisTCP.string_to_hex(exp_name)
        hex_rep += self.NanonisTCP.to_hex(len(basename),4)
        hex_rep += self.NanonisTCP.string_to_hex(basename)
        hex_rep += self.NanonisTCP.to_hex(len(ext_VI_path),4)
        hex_rep += self.NanonisTCP.string_to_hex(ext_VI_path)
        hex_rep += self.NanonisTCP.float32_to_hex(premeasure_delay)
        hex_rep += self.NanonisTCP.to_hex(save_scan_channels,4)
        
        self.NanonisTCP.send_command(hex_rep)
        
        self.NanonisTCP.receive_response(0)
        
    def PropsGet(self):
        """
        Returns the configuration of the Grid experiment section in the Scan module.

        Returns
        -------
        list_of_exp             : list of experiments available in the section "Pattern".
        exp                     : name of the selected experiment.
        ext_VI_path             : path of the external VI
        premeasure_delay        : the time (s) to wait on each point before performing the experiment.
        save_scan_channels      : indicates if the scan channels are saved into the grid experiment file.
                                :   0: Off
                                :   1: On

        """
        hex_rep = self.NanonisTCP.make_header('Pattern.PropsGet', body_size=0)
        
        self.NanonisTCP.send_command(hex_rep)
        
        response = self.NanonisTCP.receive_response()
        
        # size_list_of_exp = self.NanonisTCP.hex_to_int32(response[0:4])        # Useless
        num_exp = self.NanonisTCP.hex_to_int32(response[4:8])
        # Loop over all experiment names
        list_of_exp = []
        idx = 8
        for i in range(num_exp):
            listed_exp_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
            idx += 4
            list_of_exp.append(response[idx:idx+listed_exp_size].decode())
            idx += listed_exp_size
        
        exp_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        idx += 4
        exp = response[idx:idx+exp_size].decode()
        idx += exp_size

        ext_VI_path_size = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        idx += 4
        ext_VI_path = response[idx:idx+ext_VI_path_size].decode()
        idx += ext_VI_path_size

        premeasure_delay = self.NanonisTCP.hex_to_float32(response[idx:idx+4])
        idx += 4
        save_scan_channels = self.NanonisTCP.hex_to_int32(response[idx:idx+4])
        
        return [list_of_exp, exp, ext_VI_path, premeasure_delay, save_scan_channels]