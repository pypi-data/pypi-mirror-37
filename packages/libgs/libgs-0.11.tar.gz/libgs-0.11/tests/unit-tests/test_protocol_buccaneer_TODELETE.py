# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 15:24:55 2017

Unit tests for buccaneer protocol module


@author: kjetil
"""

import sys, os
from os.path import dirname


#
# Make sure the files one path level up are importable
#
_adfags_path = dirname(dirname(dirname(os.path.realpath(__file__)))) + '/src/adfagslib/'
sys.path.insert(0, _adfags_path)

from utils import Error, Defaults, hex2bytes, bytes2hex, bytes2prettyhex, setup_logger
from protocols.buccaneer import Spacelink
import pytest
import time
import logging
from multiprocessing import Process
import zmq

SPACELINK_PORT_PUB=6000
SPACELINK_PORT_RECV=6002
SPACELINK_ADDR_SEND='127.0.0.1:6001'
SPACELINK_ADDR_STATE='http://127.0.0.1:9051'

SCONTROL_ADDR_SPACELINK = "http://localhost:9001"
SCONTROL_ADDR_RADIO = "http://localhost:9002"

SLINK_SATID = 171
SLINK_GSID = 1

log = logging.getLogger("adfags-log")#test_communications_spacelink")
setup_logger(log, 
             cons_loglvl=logging.DEBUG, 
             file_logpath=None)


from emulators import Rotctld, BuccaneerSpacelink


# A flag to check if reply has been received
reply_received = None
sl = None

def receive_reply(msg):
    global reply_received
    reply_received = msg

emulator= None
def setup_emulator():
    try:
        BuccaneerSpacelink()
    except zmq.error.ZMQError:
        log.info("Buccaneer+Spacelink emulator already running")
        pass


@pytest.fixture
def spacelink():
    global sl
    if sl is None:
        sl = Spacelink(\
            pub_port=SPACELINK_PORT_PUB,
            recv_port=SPACELINK_PORT_RECV,
            send_addr=SPACELINK_ADDR_SEND,
            state_addr=SPACELINK_ADDR_STATE,
            satID=SLINK_SATID,
            #gsID=SLINK_GSID, 
            monitor_sockets=True,
            servcon_spacelink = SCONTROL_ADDR_SPACELINK,
            servcon_radio = SCONTROL_ADDR_RADIO,
            msghandler=receive_reply)

    return sl


def test_simple_comms(spacelink,  emulate_sl=True):
    """
    A simple py.test script to check whether basic communication through
    the protocol works.

    """

    global reply_received, emulator
    CONNECTION_TIMEOUT = 20

    # To properly unit test do not rely on spacelinik/
    if emulate_sl:
        log.info("Emulating spacelink + spacecraft")
        #if emulator is not None:
        #    emulator.terminate()
        #emulator = Process(target= setup_emulator)
        #emulator.daemon = True
        #emulator.start()
        setup_emulator()



    sl = spacelink

    sl.start_comms()

    assert sl.get_state() == 'States.connected'
    log.info('State == States.connected')

    sl.send_cmd(hex2bytes('DC-00-00-00-01-0D-00-00-00-00-25-60'))

    t0 = time.time()
    reply_received = None
    while reply_received is None:
        time.sleep(0.1)

        if time.time() - t0 > CONNECTION_TIMEOUT:
            raise Exception("Timout waiting for reply")


    log.info('Reply received: %s'%bytes2prettyhex(reply_received))
    # Check reply

    assert reply_received == '\xd3\x00@\x00\x11\x02\x01\x01\x10\x00\x00\x0f\x00\x00\x00\x000u\x00\x00 N\x00\x00\x0f\x1e5.\xf8S\x00\x00\xe0\xed\xd0\x1a\xa02\xbf6\x02\x00\x02\x00\x03\x0f\x91\x96\x9b\xa0OSPACEGROUND\x00\x03\x82\x00\xdc\x05\xdc\x05\x8a$'

    sl.stop_comms()

    assert sl.get_state() == 'States.idle'
    log.info('State == States.idle')


def test_escape(spacelink,  emulate_sl=True):

    global emulator

    # To properly unit test do not rely on spacelinik/

    if emulate_sl:
        log.info("Emulating spacelink + spacecraft")
#        if emulator is not None:
#            emulator.kill()
#        emulator = Process(target= setup_emulator)
#        emulator.daemon = True
#        emulator.start()
        setup_emulator() #<--- for some reason it doesnt work if its in a separate process


    sl = spacelink

    sl.start_comms()
    assert sl.get_state() == 'States.connected'

    sl.escape()





if __name__ == '__main__':

    sl = spacelink()

    import code
    code.interact(local=locals())

    # test_simple_comms(sl, emulate_rotctl=False)
