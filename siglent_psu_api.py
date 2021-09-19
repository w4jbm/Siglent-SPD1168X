# Siglent SPD1168X Status and Control API
#
# Based on version for the dual supply version
# by Saulius Lukse, Copyright 2015-2018
#
# This adaptation is by Jim McClanahan, W4JBM
# Copyright 2021
#
# Licensed under GNU GPLv3

import socket
import sys
import time
from enum import Enum

class MODE(Enum):
    CV  = 1
    CC  = 2

class TRACK(Enum):
    INDEPENDENT  = 0
    SERIAL = 1
    PARALLEL = 2

class STATE(Enum):
    OFF = 0
    ON = 1

class CHANNEL(Enum):
    CH1 = 1
#   CH2 = 2
#   CH3 = 3

class PARAMETER(Enum):
    CURRENT = 1
    VOLTAGE = 2
    POWER = 3

class SIGLENT_PSU():

    def __init__(self, ip, port=5025):
        self.ip = ip
        self.port = port
        self._sleep = 1
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(1)
        self.s.connect((self.ip , self.port))

    def identify(self):
        self.s.sendall(b'*IDN?')
        #self.s.sendall(b'\n')
        reply = self.s.recv(4096).decode('utf-8').strip()
        reply = reply.split(",")
        reply_d = {}
        if len(reply) == 5:
            reply_d["manufacturer"] = reply[0]
            reply_d["model"] = reply[1]
            reply_d["sn"] = reply[2]
            reply_d["firmware_ver"] = reply[3]
            reply_d["hadrware_ver"] = reply[4]
            return reply_d
        return None

    def measure(self, ch, parameter):
        cmd = "MEASURE:" + parameter.name + "? " + ch.name
        cmd_b = cmd.encode("utf-8")
        self.s.sendall(cmd_b)
        #self.s.sendall(b'\n')
        time.sleep(self._sleep)
        reply = self.s.recv(4096).decode('utf-8').strip()
        reply = float(reply)
        return reply
   
    def set(self, ch, parameter, value):
        if parameter == PARAMETER.POWER:
            raise ValueError("Can't set POWER. Only VOLTAGE and CURRENT are supported.")

        if ch != CHANNEL.CH1:
            raise ValueError("Only single channel supply supported.")            

        cmd = ch.name + ":" + parameter.name + " " + str(value)
        cmd_b = cmd.encode("utf-8")
        self.s.sendall(cmd_b)
        #self.s.sendall(b'\n')
        time.sleep(self._sleep)

    def output(self, ch, status):
        cmd = "OUTPUT " + ch.name + "," + status.name
        cmd_b = cmd.encode("utf-8")
        self.s.sendall(cmd_b)
        #self.s.sendall(b'\n')
        time.sleep(self._sleep)

#   def track(self, tr):
#       cmd = "OUTPUT:TRACK " +  str(tr.value)
#       cmd_b = cmd.encode("utf-8")
#       self.s.sendall(cmd_b)
#       #self.s.sendall(b'\n')
#       time.sleep(self._sleep)

    def system(self):
        cmd = "SYSTem:STATus?"
        cmd_b = cmd.encode("utf-8")
        self.s.sendall(cmd_b)
        #self.s.sendall(b'\n')
        time.sleep(self._sleep)
        reply = self.s.recv(4096).decode('utf-8').strip()
        reply = int(reply, 16)

        response = {}
        
        response["status"] = "0x%0.2X" % reply
        
        if reply & 0x01:
            response["mode"] = "CC"
        else:
            response["mode"] = "CV"

        if reply & 0x10:
            response["output"] = "on"
        else:
            response["output"] = "off"

        if reply & 0x20:
            response["wire_mode"] = "4W"
        else:
            response["wire_mode"] = "2W"

        if reply & 0x40:
            response["timer"] = "on"
        else:
            response["timer"] = "off"

        if reply & 0x100:
            response["display"] = "waveform"
        else:
            response["display"] = "digital"

        return response

