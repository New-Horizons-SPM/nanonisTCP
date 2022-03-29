#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 16:56:08 2022

@author: jack
"""


from NanonisTCP import Bias, FolMe, NanonisTCP

TCP_IP = '127.0.0.1'
TCP_PORT = 6501

NTCP = NanonisTCP(TCP_IP, TCP_PORT)
bias = Bias(NTCP)

bias.Set(7)

# NTCP.close_connection()

followme = FolMe(NTCP)

answer = followme.XYPosSet(50e-9, -300e-9, Wait_end_of_move=False)
NTCP.close_connection()