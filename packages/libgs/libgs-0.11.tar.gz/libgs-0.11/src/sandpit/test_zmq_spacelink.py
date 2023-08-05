# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:47:15 2017

@author: kjetil
"""

import zmq
import time

import threading
import struct
import binascii
import datetime
import pmt
import numpy as np

CMD = {\
    "GeneralGetTelemetry": {
        'cmd':  "DC-00-00-00-01-13-00-00-00-00-D7-AB",
        'resp': "D3-00-44-00-10-03-00-00-00-00-00-00-00-00-47-26-01-00-15-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-23-00-63-01-F2-03-00-00-4B-06-00-00-27-3C-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-D6-32-"},
    "GeneralCommGetConfigCommand" : {
        'cmd':  "DC-00-00-00-01-0D-00-00-00-00-25-60-",
        'resp': "D3-00-40-00-11-02-01-00-10-00-00-0F-00-00-00-00-E0-93-04-00-20-4E-00-00-0F-1E-35-2E-F8-53-00-00-E0-ED-D0-1A-A0-32-BF-36-02-00-02-00-03-0F-91-96-9B-A0-4F-53-50-41-43-45-47-52-4F-55-4E-44-00-03-02-00-DC-05-DC-05-38-5E-"},
    "GeneralCmdLogGetDataCommand" : {
        'cmd':  "DC-00-07-00-01-05-00-00-00-00-FF-FF-FF-FF-05-01-00-2F-9E-",
        'resp': "D3-00-12-00-13-0F-E3-75-B7-05-01-00-07-00-01-05-00-00-00-00-00-00-00-00-67-87-D3-00-12-00-13-0F-DB-75-B7-05-01-00-07-00-01-05-00-00-00-00-00-00-00-00-28-71-D3-00-12-00-13-0F-BB-75-B7-05-01-00-00-00-01-04-00-00-00-00-00-00-00-00-00-9C-D3-00-12-00-13-0F-A6-75-B7-05-01-00-01-00-01-04-00-00-00-00-09-00-00-00-04-6F-D3-00-12-00-13-0F-93-75-B7-05-01-00-01-00-01-0D-00-00-00-00-09-00-00-00-6E-AA-"},
    "SystemSettimeCommand": {
        'cmd': "DC-00-04-00-05-02-00-00-00-00-A9-30-B8-05-F4-17",
        'resp': ""}
    }


        
class Error(Exception):
    """Generic Error for this module"""

    def __init__(self, msg, original_Error=None):
        if original_Error is not None:
            super(Error, self).__init__(msg + (": %s" % original_Error))
            self.original_Error = original_Error
        else:
            super(Error, self).__init__(msg)    



if 1:
    # Other commands (no resonse)
    # 0x06: GeneralCmdLogClear
    #

    #General
    resp01 = {
    
        # General status (with data=0x01)
        0x01: (\
            [0xD3, 0x00, 0x0E, 0x00, 0x11, 0x01, 0x00, 0x8D, 0x27, 0x00, 0x00, 0x37, 0x00, 0x00, 0xFF, 0x36, 0x00, 0x00, 0x00, 0x00, 0x53, 0x88],
            [0xD3, 0x00, 0x0E, 0x00, 0x11, 0x01, 0x00, 0x8D, 0x27, 0x00, 0x9A, 0x38, 0x00, 0x00, 0x99, 0x38, 0x00, 0x00, 0x00, 0x00, 0x35, 0xE9]
            ),
            
        #GeneralGetTelemetry
        0x13: (\
            [0xD3, 0x00, 0x44, 0x00, 0x10, 0x03, 0x00, 0x8D, 0x27, 0x00, 0x1C, 0x49, 0x00, 0x00, 0x4C, 0x26, 0x01, 0x00, 0x0E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4E, 0x00, 0x65, 0x01, 0xA6, 0x02, 0x00, 0x00, 0x91, 0x04, 0x00, 0x00, 0x26, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x97, 0xE7]
            ),
        
        #GeneralCommGetConfigCommand
        0x0d: (\
            [0xD3, 0x00, 0x40, 0x00, 0x11, 0x02, 0x01, 0x01, 0x10, 0x00, 0x00, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x30, 0x75, 0x00, 0x00, 0x20, 0x4E, 0x00, 0x00, 0x0F, 0x1E, 0x35, 0x2E, 0xF8, 0x53, 0x00, 0x00, 0xE0, 0xED, 0xD0, 0x1A, 0xA0, 0x32, 0xBF, 0x36, 0x02, 0x00, 0x02, 0x00, 0x03, 0x0F, 0x91, 0x96, 0x9B, 0xA0, 0x4F, 0x53, 0x50, 0x41, 0x43, 0x45, 0x47, 0x52, 0x4F, 0x55, 0x4E, 0x44, 0x00, 0x03, 0x82, 0x00, 0xDC, 0x05, 0xDC, 0x05, 0x8A, 0x24]
            ),
            
        #GeneralCmdLogGetDataCommand 
        0x05: (\
            # create_cmd_seq(0x05, 0x01, [0xff, 0xff, 0xff, 0xff, 5, 0x00, 0x00])
            [0xD3, 0x00, 0x12, 0x00, 0x13, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x05, 0x00, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0xA5, 0xAC, 0xD3, 0x00, 0x12, 0x00, 0x13, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x0D, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2D, 0x76, 0xD3, 0x00, 0x12, 0x00, 0x13, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA4, 0x56, 0xD3, 0x00, 0x12, 0x00, 0x13, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x48, 0xC0],

            #create_cmd_seq(0x05, 0x01, [0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00]
            [0xD3, 0x00, 0x12, 0x00, 0x13, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x48, 0xC0, 0xD3, 0x00, 0x12, 0x00, 0x13, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x06, 0x00, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x47, 0xE5, 0xD3, 0x00, 0x12, 0x00, 0x13, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x06, 0x00, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x47, 0xE5, 0xD3, 0x00, 0x12, 0x00, 0x13, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x48, 0xC0, 0xD3, 0x00, 0x12, 0x00, 0x13, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF2, 0x72, 0xD3, 0x00, 0x12, 0x00, 0x13, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x05, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x6E, 0xD3, 0x00, 0x00, 0x00, 0x13, 0x0F, 0x8B, 0xC3],

            #AFTER sendinc command 0x06 (clear log) : create_cmd_seq(0x05, [0xff, 0xff, 0xff, 0xff, 5, 0x00, 0x00])
            [0xD3, 0x00, 0x12, 0x00, 0x13, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x96, 0x72]
            ),
        
        #GeneralCmdLogGetStatusCommand
        #create_cmd_seq(0x04)
        0x04: (\
            
        )
        
        #SystemGetStatus
        }
      
    # System
    resp05 = {
    
        #SystemGetStatus
        #create_cmd_seq(0x01, 0x05, [])
        0x01: (
            [0xD3, 0x00, 0x2C, 0x00, 0x50, 0x01, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0xDE, 0x3A, 0x4B, 0x00, 0x1B, 0x00, 0x00, 0x00, 0x02, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x00, 0x02, 0x13, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x82, 0xE8],

            #a bit after setting the time to [0xA9, 0x30, 0xB8, 0x05]
            [0xD3, 0x00, 0x2C, 0x00, 0x50, 0x01, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x96, 0x8C, 0x00, 0x00, 0x1E, 0x00, 0x00, 0x00, 0x02, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x01, 0x00, 0x02, 0x16, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0xB3, 0x4B]),
    
        #SystemSetTime
        #// The sructure of the system time type is as follows:
        #//	31:26	Years since SYS_RTCC_BASE_YEAR (max value is 63 years)
        #//	25:22	Month
        #//	21:17	Day of month
        #//	16:12	Hours
        #//	11:6	Minutes
        #//	 5:0	Seconds
        # I think SYS_RTCC_BASE_YEAR is 2016
        #
        # create_cmd_seq(0x02, 0x05, [0xA9, 0x30, 0xB8, 0x05])
        # Sets time to 2017-06-28 03:02:41
        0x02: (),
    
        #SystemGetTelemetry
        # create_cmd_seq(0x12, 0x05, [])
        0x12: ([0xD3, 0x00, 0x6A, 0x00, 0x50, 0x03, 0xFF, 0x03, 0x21, 0x03, 0xF8, 0x00, 0x82, 0x02, 0x4D, 0x01, 0xFF, 0x03, 0x32, 0x03, 0xF5, 0x00, 0x81, 0x02, 0x50, 0x01, 0xFF, 0x03, 0x2C, 0x03, 0xF4, 0x00, 0x81, 0x02, 0x4E, 0x01, 0x36, 0x03, 0x02, 0x00, 0x10, 0x00, 0x0D, 0x00, 0x2B, 0x03, 0x30, 0x03, 0x80, 0x03, 0x02, 0x00, 0x34, 0x03, 0xAA, 0x00, 0x5B, 0x03, 0x0A, 0x00, 0x04, 0x03, 0x13, 0x00, 0x02, 0x00, 0x02, 0x00, 0x02, 0x00, 0x02, 0x00, 0x02, 0x00, 0x03, 0x00, 0x02, 0x00, 0x03, 0x00, 0x9C, 0x02, 0x03, 0x00, 0x03, 0x00, 0x03, 0x00, 0x9C, 0x02, 0x9E, 0x02, 0x02, 0x00, 0x01, 0x00, 0x02, 0x00, 0xA1, 0x02, 0x9F, 0x02, 0x03, 0x00, 0x03, 0x00, 0x03, 0x00, 0x9C, 0x02, 0x9D, 0x02, 0xDE, 0xE9])
    
    }
    
def encode_time(t):
    if type(t) != datetime.datetime:
        raise Exception('wrong type')
    
    YEARS = ((t.year - 2016) & 0b111111) << 26
    MONTH = t.month << 22
    DAY   = t.day << 17
    HOURS = t.hour << 12
    MINS  = t.minute << 6
    SECS  = t.second
    
    print("YEARS: {:32b}".format(YEARS))
    print("MONTH: {:32b}".format(MONTH))
    print("DAY:   {:32b}".format(DAY))
    print("HOURS: {:32b}".format(HOURS))
    print("MINS:  {:32b}".format(MINS))
    print("SECS:  {:32b}".format(SECS))    
    
    encoded = YEARS | MONTH | DAY | HOURS | MINS | SECS
    
    return encoded

def decode_time(t):
    
    YEARS = (t >> 26) & 0b111111
    MONTH = (t >> 22) & 0b1111
    DAY   = (t >> 17) & 0b11111
    HOURS = (t >> 12) & 0b11111
    MINS  = (t >> 6) &  0b111111
    SECS  = (t ) &  0b111111
    
    print("YEARS: {:32b}".format(YEARS << 26))
    print("MONTH: {:32b}".format(MONTH << 22))
    print("DAY:   {:32b}".format(DAY << 17))
    print("HOURS: {:32b}".format(HOURS << 12))
    print("MINS:  {:32b}".format(MINS << 6))
    print("SECS:  {:32b}".format(SECS))    
    
    
    return datetime.datetime(
        YEARS + 2016, MONTH, DAY, HOURS, MINS, SECS
        )


#sys time example above 
example_time = decode_time(struct.unpack('<L', b'\xA9\x30\xB8\x05')[0])


def decode_response(resp):
    
    resps = bytearray(resp)#''.join([struct.pack('B', x) for x in resp])
    # This byte is overwritten by SpaceLink as a synch byte. Set to 0x00.
    SYNC = resps[0]
    
    RES_E = resps[1]
    #These bits are reserved for future use and should always be set to zero.
    RES = (RES_E & 0b11111110) >> 1
    
    #This 1-bit flag indicates whether the response (byte 4 onwards) is encrypted (1) or not encrypted (0). The encryption used is AES-256 CTR (counter) mode encryption.
    E = (RES_E & 0b1)

    #The DATA LENGTH field is a 16-bit unsigned integer defining the length of the data field.  A data length of zero indicates that there is no data field.
    DLEN, = struct.unpack('<H', resps[2:4])

    #The RESP CODE field is a 16-bit unsigned integer indicating the type of response. The available response codes are listed in Table 3 1.
    RESP_CODE, = struct.unpack('<H', resps[4:6])

    #Data 
    DATA = resps[6:6+DLEN]

    #The CRC checksum
    CRC, = struct.unpack('<H', resps[6+DLEN:6+DLEN+2])
    
    #check crc
    crc_check = binascii.crc_hqx(resps[0:6+DLEN], 0xffff)
    
    if CRC == crc_check:
        print('CRC verification passed')
    else:
        print('CRC verification failed')
        
    return RESP_CODE, DATA

def decode_GENERAL__TAP_GET_STATUS(data):
    if len(data) != 14:
        raise Exception('data has incorrect length')
    print("Max size of TAP region:             %d"%(struct.unpack('<L', (data[0:4]))))
    print("Number of TAPs currently available: %d"%(struct.unpack('<L', (data[4:8]))))
    print("Index of last TAP written:          %d"%(struct.unpack('<L', (data[8:12]))))
    print("Init Error status:                  %d"%(struct.unpack('<H', (data[12:14]))))



if 0:
    # 1) BASED ON READING MANUAL
    data0 = [\
        chr(0x00), #SYNC
        chr(0b00000000), #Receive via UHF, not encr
        struct.pack('>H', 0), #no data
        chr(0x01), #General subsystem
        chr(0x01), #GENERAL__TAP_GET_STATUS
        struct.pack('>I', 0)] #RUNTIME - 0x00 means run immediately
        
    crc0 = binascii.crc_hqx(''.join(data0), 0xffff)
    
    msg0 = ''.join(data0 + [struct.pack('>H', crc0)])

if 0:
    # 2) DIRECTLY FROM NATALIE
    # - looks encrypted!


    # Valid message for GENERAL_TAP_GET_STATUS
    # REceived from DST group:
    # DC-00-01-00-01-01-00-00-00-00-01-47-B9
    data = [0xDC,0x00,0x01,0x00,0x01,0x01,0x00,0x00,0x00,0x00,0x01,0x47,0xB9]
    msg =  ''.join([struct.pack('>B', d) for d in data])

if 0:
    # 3) BASED ON REVERSE-ENGINEERING it seems to me that byte order is opposite
    # to 1)

    # Here is Natalieś message
    data1 = [0xDC,0x00,0x01,0x00,0x01,0x01,0x00,0x00,0x00,0x00,0x01]
    data1s =  [struct.pack('B', d) for d in data[:-2]]
    crc1 = binascii.crc_hqx(''.join(data1s), 0xffff)
    msg1 = ''.join(data1s + [struct.pack('<H', crc1)])
    
# So assuming reversed byte order to 1), this function should generate valid
# commands

def create_cmd_seq(cmd, sub=0x01, data=[]):
    """
        This function is based on the command and tlemetry handbook,
        but also by reverse-engineering known command sequences
        
        The comments are from the C&T handbook.
        
        I discovered that byte-ordre is little-endian!
    """

    #Overwritten by spacelink apparently
    SYNC = struct.pack('B',0xdc)
    
    #These bits are reserved for future use and should always be set to zero.
    RES = 0b0000
    
    #This two-bit field specifies the communication link to use for the response
    #0 = UHF, 1 =STX.
    RC = 0b00
    
    #This 1-bit flag indicates whether the response is to be encrypted (1) or not encrypted (0).
    RE = 0b0
    
    #This 1-bit flag indicates whether the command (byte 4 onwards) is encrypted (1) or not encrypted (0). 
    E = 0b0
    
    RC_RE_E = struct.pack('B', (RES << 4) | (RC << 2) | (RE << 1) | E)

    
    #The DATA LENGTH field is a 16-bit unsigned integer defining the length of the data field.  A command that does not have any data will specify a length of ‘0’.

    #Data
    if len(data) > 0xffff:
        raise Exception('len(data) cannot exceed 0xffff')

    DLEN = struct.pack('<H', len(data))
    
    #The SUB field is a 3-bit value representing the subsystem to be commanded. 
    SUB = struct.pack('B', sub)
    

    #The CMD field is an 8-bit integer representing the command code to apply to the specified subsystem
    CMD = struct.pack('B', cmd)
    
    #The RUNTIME field is a 32-bit unsigned integer value specifying the time at which the command must be executed. 0 = now
    RTIME = struct.pack('<L', 0)
    
    #The data field is a variable length field, containing the number of bytes specified in the ‘Length’ field.  When length is ‘0’ there is no data.
    DATA = ''.join([struct.pack('B', d) for d in data])


    #Create command bytestr
    cmdstr = SYNC + RC_RE_E + DLEN + SUB + CMD + RTIME + DATA
    
    #Compute crc
    crc = binascii.crc_hqx(cmdstr, 0xffff)
    
    # append CRC
    cmdstr += struct.pack('<H', crc)


    return cmdstr
    
    #This 2-byte field is a 16-bit cyclic redundancy checksum of the header, preamble and data bytes of the command packet.  The algorithm used is CCITT16 with polynomial 0x1021 (x16 + x12 + x5 + 1).
    


if 1:
    ##publishing socket
    context = zmq.Context()
    
if 0:
    socket0 = context.socket(zmq.PUB)
    socket0.bind("tcp://*:%s" % 6000)
    #

    socket1 = context.socket(zmq.REQ)
    socket1.bind("tcp://*:6002")

if 0:
    socket1 = context.socket(zmq.PAIR)
    socket1.connect("tcp://127.0.0.1:6011")    
    
if 0:    
    # receiving socket
    socket2 = context.socket(zmq.SUB)
    socket2.connect("tcp://127.0.0.1:6000")
    
    socket2.setsockopt(zmq.SUBSCRIBE, "ETX")
    socket2.setsockopt(zmq.SUBSCRIBE, "STX")
    
    
    socket3 = context.socket(zmq.REP)
    socket3.connect("tcp://127.0.0.1:6001")
    
if 0:
    socket4 = context.socket(zmq.PULL)
    socket4.connect("tcp://127.0.0.1:5501")


if 0:
    s1 = context.socket(zmq.SUB)
    s1.connect("tcp://127.0.0.1:5560")
    s1.setsockopt(zmq.SUBSCRIBE, '')

if 1:
    
    # Create receiver thread
    
    def recv_thread():
        
        poller = zmq.Poller()
        poller.register(s1)
        
        
        i = 0
        while i < 2:
            socks = poller.poll(1000)
            
            for s, event in socks:
                x = s.recv()
                dx = pmt.deserialize_str(x)
                print ("%6d: "%(i) + bytes(x).encode("string-escape"))
                
                i += 1


    # Listen in on GNU Radio messages

    stop_threads = False     
    s1 = context.socket(zmq.SUB)           
    s1.connect("tcp://127.0.0.1:5560")
    s1.setsockopt(zmq.SUBSCRIBE, '')

    s2 = context.socket(zmq.SUB)
    s2.connect("tcp://127.0.0.1:5561")
    s2.setsockopt(zmq.SUBSCRIBE, '')

    s3 = context.socket(zmq.SUB)
    s3.connect("tcp://127.0.0.1:5551")
    s3.setsockopt(zmq.SUBSCRIBE, '')


    def recv_thr1():
        
        fp1 = open("port_5560.bin", "wb")
        
        while(stop_threads is False):
            x = s1.recv()
            fp1.write(x)


    def recv_thr2():            
        fp1 = open("port_5561.bin", "wb")
        
        while(stop_threads is False):
            x = s2.recv()
            fp1.write(x)





    def rt3():              
        #fp1 = open("port_5551.bin", "wb")
        
        while(stop_threads is False):
            x = s3.recv()
            y = np.frombuffer(x, dtype=np.complex64)
            rt3.yf = np.fft.fftshift(np.fft.fft(y))
            rt3.freq = np.fft.fftfreq(len(y), d = 1.0/32000)
            rt3.freq = np.fft.fftshift(rt3.freq)
            
            #fp1.write(x)

            #time.sleep(1)
                
    #p1 = threading.Thread(target=recv_thr1)
    #p2 = threading.Thread(target=recv_thr2)
    p3 = threading.Thread(target=rt3)
    #p1.start()
    #p2.start()
    p3.start()

if 1:
    # Ref:
    import pmt
    s='\n\x08\x00\x00\x00\x01\x01\x00?\xe4\xbe\x83\x00\x00\x00\x00'
    p = pmt.deserialize_str(s)
    python_numpy_array = pmt.pmt_to_python.pmt_to_python(p)

    # Now try with some recorded data
    fp = open('./comms_tests/test1_20170720_0005/port_5551.bin', 'rb')
    d = fp.read()
    fp.close()

    GR_HEADER_MAGIC = 0x5FF0
    GR_HEADER_VERSION = 0x01
    
    header_magic, = struct.unpack('<H',d[0:2])
    header_version, = struct.unpack('B', d[3])
    
    

    # TODO: Try with recv multipart

class Spacelink():
    """
    Class to handle communication between adfags and a spacelink service
    (that again will communicate with the spacecraft through GNU radio)
    
    It is configured by connecting to the spacelink service on the appropriate
    addresses
    
    Args:
        pub_port (int, optional):   The port to broadcast communication requests on
                                    The default is port 6000
        recv_port (int, optional):  The port on which to receive data
                                    The default is port 6002
        send_addr (int, optional):  The address on which the spacelink service
                                    is listening. The default is '127.0.0.1:6001'
        satID (int, optional):      The spacelink ID of the satellite to connect to
                                    (set in spacelink.json in th dst module)
        gsID (int, optional):       The spacelink ID of the ground station 
                                    (set in spacelink.json in the dst module)
    """
    
    def __init__(self,
                 pub_port=6000, 
                 recv_port=6002, 
                 send_addr='127.0.0.1:6001', 
                 satID=171, 
                 gsID=1, 
                 monitor_sockets=True):
        
        # poll timeout in milliseconds
        self._poll_timeout = 1000    
        
        # Addresses
        self.pub_addr = 'tcp://*:%s'%(str(pub_port))
        self.send_addr = 'tcp://%s'%(send_addr)
        self.recv_addr = 'tcp://*:%s'%(str(recv_port))
        
        # Monitor sockts
        self._monitor = monitor_sockets

        # Keep track of socket status
        self.sock_status = {'recv': None, 'send':None, 'pub':None}


        # Initialise the context and sockets
        self._init_context()
        


    def _init_context(self):
        self.ctx = zmq.Context()
        
        
        self._sock_pub = self.ctx.socket(zmq.PUB)
        self._sock_send = self.ctx.socket(zmq.REQ)
        self._sock_recv = self.ctx.socket(zmq.REP)
        
        # Create monitor sockets
        if self._monitor is True:
            self._monitor_pub = self._sock_pub.get_monitor_socket()
            self._monitor_send = self._sock_send.get_monitor_socket()
            self._monitor_recv = self._sock_recv.get_monitor_socket()
            
            self._pthr_mon = threading.Thread(target=self._mon_thread)
            self._pthr_mon.start()
        
        # If something goes wrong in the middle of a REQ/REP pattern, the 
        # socket gets into an unusable state. This can be handled with the
        self._sock_send.setsockopt(zmq.REQ_RELAXED, 1)
        self._sock_send.setsockopt(zmq.REQ_CORRELATE, 1)

        # Timeout period when waiting for ack. Handled with pollin gon the recv
        # socket
        self._sock_send.setsockopt(zmq.RCVTIMEO, 1000)
        self._sock_pub.setsockopt(zmq.RCVTIMEO, 1000)

        # Bind sockets
        self._sock_recv.bind(self.recv_addr)
        self._sock_pub.bind(self.pub_addr)
        
        
    def _mon_thread(self):
        """
        
        """
        poller = zmq.Poller()
        poller.register(self._monitor_pub, zmq.POLLIN)   
        poller.register(self._monitor_send, zmq.POLLIN)
        poller.register(self._monitor_recv, zmq.POLLIN)

        EVENT_MAP = {}
        for name in dir(zmq):
            if name.startswith("EVENT_"):
                value = getattr(zmq,name)
                EVENT_MAP[value] = name        

        self._stop_monitor = False
        
        while (self._stop_monitor is False):
            sock = poller.poll(self._poll_timeout)
            
            for s, event in sock:
                if (event & zmq.POLLIN) != 0:
                    msg = s.recv_multipart()
                    event, value =  struct.unpack("=hi", msg[0])
                    endpoint = msg[1]
                             
                    #self._print("  %5d: %30s: %s"%(evt['value'], evt['endpoint'], EVENT_MAP[evt['event']]))
            
                    if endpoint == self.send_addr:
                        self.sock_status['send'] = EVENT_MAP[event]                        
                    elif endpoint[-4:] == self.recv_addr[-4:]:
                        self.sock_status['recv'] = EVENT_MAP[event]
                    elif endpoint[-4:] == self.pub_addr[-4:]:
                        self.sock_status['pub'] = EVENT_MAP[event]
                    else:
                        self._print("  %5d: Unexp endpoint: %30s: %s"%(value, endpoint, EVENT_MAP[event]))
                                    
                                        
                    
            time.sleep(0.1)
        
    

    def _recv_thread(self):
        """
            Receiver thread
        """
        poller = zmq.Poller()
        poller.register(self._sock_recv, zmq.POLLIN)
    
        #poller.register(self._sock_send, zmq.POLLIN)
        #poller.register(self._sock_pub, zmq.POLLIN)
        
        self._stop_recv = False
        while (self._stop_recv is False):
            sock = poller.poll(self._poll_timeout)
            
            for s, event in sock:
                
                # Receive a message from Spacelink service
                if s == sock._sock_recv:
                    cmd, satID, data = s.recv_multipart()
                    s.send(b'ack')
                    
                    sid, = struct.unpack('<B', satID)
                    
                    self._handle_msg(cmd, sid, data)
                    
                else:
                    raise Error('Unexpected 0mq socket')
        

            time.sleep(0.1)        
            
    def _print(self, *args):
        print(args[0])
        
    def _print_msg(self, cmd, satID, data):
        """
            Function to print (stdout/log) a command and its data
            
        """
        st = "Message %s"%(cmd)
        if satID is not None:
            st += " for %d"%(satID)
            
        if data is None:
            st += " (no data)"
            
        self._print(st)
        
        if data is not None:
            data_array = map(ord, data)
            datastr=["%02X"%(x) for x in data_array]
            N = range(0, len(datastr), 10)
            for n in N:
                self._print('  '+"-".join(datastr[0+n:10+n]))        

    def _handle_msg(self, cmd, satID, data):
        
        self._print_msg(cmd, satID, data)
        

    
    def _connect(self):
        """
        Connect to send socket and start receiver thread
        """
        self._sock_send.connect(self.send_addr)
        self._pthr_recv = threading.Thread(target=self._recv_thread)
        self._pthr_recv.start()
    
    def _disconnect(self):
        
        self._sock_send.disconnect(self.send_addr)
        
        # stop thread...
        self._stop_recv = True
        
        

    def start_comms(self):
        """
        Connect to send socket, start receiver thread, and connect to satellite
        """
        # connect to socket
        self._connect()
        
        # connect to satellite
        self._sock_pub.send_multipart(['STX', ''])
        
        # Some form of feedback here would be good - to check state of spacelink


    def stop_comms(self):
        self._sock_pub.send_multipart(['ETX', ''])
        
        self._disconnect()
        
        

    def escape(self):
        # not sure if this works. SHould be an emergency stop
        self._sock_pub.send_multipart(['ESC', ''])
        
        self._disconnect()

    def send_cmd(self, msg):
        
        sid = self.satID
        #print(['DTR', struct.pack('<B', sid), msg])
        #print("Sending DTR addressed to satID %d: %s"%(sid, msg))
        self._sock_send.send_multipart(['DTR', struct.pack('<B', sid), msg])
    
        data_array = map(ord, msg)
        print("Message sent:")
        print("  cmd=%s\n  satID=%d"%('DTR', sid))
        print("  data=%s"%(' '.join(['%X'%(x) for x in data_array])))
        print("        (%s)"%(bytes(msg).encode("string-escape")))
    

    def __del__(self):
        self._sock_pub.close()
        self._sock_recv.close()
        self._sock_send.close()
        
                

#sl = Spacelink()
