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
    
    def make_header(self, command_name, body_size, resp):
        hex_rep = command_name.encode('utf-8').hex() ## command name
        hex_rep += "{0:#0{1}}".format(0,(64 - len(hex_rep))) ## command name (fixed 32)
        hex_rep += "{0:#0{1}}".format(int(format(body_size, 'x')), 8) ## Body size (fixed 4)
        hex_rep += "{0:#0{1}}".format(resp, 4) ## Send response (fixed 2)
        hex_rep += "{0:#0{1}}".format(0, 4) ## not used (fixed 2)
        return hex_rep
    
    def send_command(self, message):
        self.s.send(message)
        
    def receive_response(self, num_bytes):
        return self.s.recv(num_bytes)
    
    def close_connection(self):
        self.s.close()
        
        

class Bias:
    NanonisTCP = {}
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def Set(self, bias, resp=False):

        ## make header
        hex_rep = self.NanonisTCP.make_header('Bias.Set', body_size=4, resp=resp)
        ## header constructed
        ## see https://stackoverflow.com/questions/23624212/how-to-convert-a-float-into-hex
        hex_rep += hex(struct.unpack('<I', struct.pack('<f', bias))[0])[2:] ## X(m) (float64) ## bias (float 32)
        
        self.NanonisTCP.send_command(bytes.fromhex(hex_rep))
        
        if resp == True:
            return self.NanonisTCP.receive_response(48) ## number of bytes specific to command



class FolMe:
    def __init__(self, NanonisTCP):
        self.NanonisTCP = NanonisTCP
    
    def XYPosSet(self, X, Y, Wait_end_of_move):
        
        ## make header
        hex_rep = self.NanonisTCP.make_header('FolMe.XYPosSet', body_size=20, resp=True)
        
        hex_rep += hex(struct.unpack('<Q', struct.pack('<d', X))[0])[2:] ## X(m) (float64)
        hex_rep += hex(struct.unpack('<Q', struct.pack('<d', Y))[0])[2:] ## Y(m) (float64)
        hex_rep += "{0:#0{1}}".format(Wait_end_of_move, 8) ## Wait end-of-move (4)
        
        self.NanonisTCP.send_command(bytes.fromhex(hex_rep))
        
        return self.NanonisTCP.receive_response(48)





