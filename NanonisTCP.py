#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:25:57 2022

@author: jack
"""

import struct

import socket


class NanonisTCP:
    IP = '127.0.0.1'
    PORT = 6501
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((IP, PORT))
    
    
    ### TCP/IP command functions
    
    def send_command(self, message):
        self.s.send(message)
        
    def receive_response(self, num_bytes):
        return self.s.recv(num_bytes)
    
    def close_connection(self):
        self.s.close()
        
    ## header & body hex message generating functions
    
    def make_header(self, command_name, body_size, resp):
        hex_rep = command_name.encode('utf-8').hex() ## command name
        hex_rep += "{0:#0{1}}".format(0,(64 - len(hex_rep))) ## command name (fixed 32)
        hex_rep += "{0:#0{1}}".format(int(format(body_size, 'x')), 8) ## Body size (fixed 4)
        hex_rep += "{0:#0{1}}".format(resp, 4) ## Send response (fixed 2)
        hex_rep += "{0:#0{1}}".format(0, 4) ## not used (fixed 2)
        return hex_rep
    

        
    def make_hex_of_float(self, value, value_type):
        '''
        https://stackoverflow.com/questions/23624212/how-to-convert-a-float-into-hex

        Parameters
        ----------
        value : float32 or float63
            value to be converted to hex.
        value_type : string
            string specifying data type, e.g. 'float32' or 'float64'

        Returns
        -------
        TYPE
            hex representation of value

        '''
        if value_type == 'float32':
            return hex(struct.unpack('<I', struct.pack('<f', value))[0])[2:]
        if value_type == 'float64':
            return hex(struct.unpack('<Q', struct.pack('<d', value))[0])[2:]
        
    # def parse_response(self, response):
    #     command = response[:32] ## 32 bytes
    #     body_size = response[32:36] ## 4 bytes
        
        
    #     not_used = response[36:40] ## 4 bytes
    #     error_status = response[40:44] ## 4 bytes
    #     error_size =
        
        

class Bias:
    NanonisTCP = {}
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def Set(self, bias, resp=False, err_length=48):

        ## make header
        hex_rep = self.NanonisTCP.make_header('Bias.Set', body_size=4, resp=resp)
        ## header constructed
        hex_rep += self.NanonisTCP.make_hex_of_float(bias, 'float32')
        
        self.NanonisTCP.send_command(bytes.fromhex(hex_rep))
        
        if resp == True:
            return self.NanonisTCP.receive_response(err_length) ## number of bytes specific to command
        
    def Get(self, response_length=48):
        
        ## make header
        hex_rep = self.NanonisTCP.make_header('Bias.Get', body_size=response_length, resp=True)
        
        self.NanonisTCP.send_command(bytes.fromhex(hex_rep))
        
        answer = self.NanonisTCP.receive_response(response_length)
        
        return answer
        
        



class FolMe:
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def XYPosSet(self, X, Y, Wait_end_of_move):
        
        ## make header
        hex_rep = self.NanonisTCP.make_header('FolMe.XYPosSet', body_size=20, resp=True)
        
        hex_rep += self.NanonisTCP.make_hex_of_float(X, 'float64') ## X(m) (float64)
        hex_rep += self.NanonisTCP.make_hex_of_float(Y, 'float64') ## Y(m) (float64)
        hex_rep += "{0:#0{1}}".format(Wait_end_of_move, 8) ## Wait end-of-move (4)
        
        self.NanonisTCP.send_command(bytes.fromhex(hex_rep))
        
        return self.NanonisTCP.receive_response(48)





