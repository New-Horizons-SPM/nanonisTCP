#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:25:57 2022

@author: jack
"""

import struct
import socket


class NanonisTCP:
    def __init__(self, IP='127.0.0.1', PORT=6501, max_buf_size=1024):
        """
        Parameters
        IP              : Listening IP address
        PORT            : Listening Port (check Nanonis File>Settings>TCP)
        max_buf_size    : maximum size of the response message. just make it big
        """
        self.IP   = IP
        self.PORT = PORT
        self.max_buf_size = max_buf_size
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              # Set up the connection
        self.s.connect((IP, PORT))                                              # Open the TCP connection.
        
    def make_header(self, command_name, body_size, resp=True):
        """
        Parameters
        command_name : name of the Nanonis function
        body_size    : size of the message body in bytes
        resp         : tell nanonis to send a response. response contains error
                       message so will nearly always want to receive it

        Returns
        hex_rep : hex representation of the header string
        """
        hex_rep = command_name.encode('utf-8').hex()                            # command name
        hex_rep += "{0:#0{1}}".format(0,(64 - len(hex_rep)))                    # command name (fixed 32)
        hex_rep += "{0:#0{1}}".format(int(format(body_size, 'x')), 8)           # Body size (fixed 4)
        hex_rep += "{0:#0{1}}".format(resp, 4)                                  # Send response (fixed 2)
        hex_rep += "{0:#0{1}}".format(0, 4)                                     # not used (fixed 2)
        return hex_rep
    
    ## Struct formatting:
    ## https://docs.python.org/3/library/struct.html#format-characters
    
    ## Hex to x conversions
    def hex_to_uint16(self,h16):
        return struct.unpack('<I', h16)[0]
    
    def hex_to_float64(self,h64):
        # see https://forum.inductiveautomation.com/t/ieee-754-standard-converting-64-bit-hex-to-decimal/9324/3
        return struct.unpack("<d", struct.pack("Q",int("0x"+h64, 16)))[0]
    
    def hex_to_float32(self,h32):
        # see https://forum.inductiveautomation.com/t/ieee-754-standard-converting-64-bit-hex-to-decimal/9324/3
        return struct.unpack("<f", struct.pack("I",int("0x"+h32, 16)))[0]
    
    ## x to hex conversions
    def float64_to_hex(self,f64):
        # see https://stackoverflow.com/questions/23624212/how-to-convert-a-float-into-hex
        return hex(struct.unpack('<Q', struct.pack('<d', f64))[0])[2:]          # float64 to hex
    
    def float32_to_hex(self,f32):
        # see https://stackoverflow.com/questions/23624212/how-to-convert-a-float-into-hex
        return hex(struct.unpack('<I', struct.pack('<f', f32))[0])[2:]          # float32 to hex
    
    def to_hex(self,conv,num_bytes):
        return "{0:#0{1}}".format(conv, 2*num_bytes)
    
    def send_command(self, message):
        """
        Parameters
        message : message to send over TCP to nanonis
        """
        self.s.send(bytes.fromhex(message))                                     # Convert hex into bytes object
        
    def receive_response(self, error_index, keep_header = False):
        """
        Parameters
        error_index : index of 'error status' within the body
        keep_header : if true: return entire response. if false: return body
        
        Returns
        response    : either header + body or body only (keep_header)
        
        Raises
        Exception   : error message returned from Nanonis
        """
        response = self.s.recv(self.max_buf_size)                               # Read the response
        
        i = error_index + 40                                                    # error_index points to start-byte in the body, which is after the 40-byte header
        error_status = self.hex_to_uint16(response[i:i+4])                      # error_status is 4 bytes long
        
        if(error_status):
            i += 8                                                              # index of error description is 8 bytes after error status
            error_description = response[i:].decode()                           # just grab from start index to the end of the message
            raise Exception(error_description)                                  # raise the exception
        
        if(not keep_header):
            return response[40:]                                                # Header is fixed to 40 bytes - drop it
        
        return response
    
    def close_connection(self):
        """
        Close the TCP connection
        """
        self.s.close()