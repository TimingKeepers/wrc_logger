#!/usr/bin/python
#/etc/sudoers add rule under sudo: 
#pi ALL=(ALL) NOPASSWD: /usr/local/bin gpio

'''
Tool to turn on and off GPIO pin

@file
@author Anne Munoz<amunoz@sevensols.com>
@date February 25, 2016
@copyright LGPL v2.1
'''


#------------------------------------------------------------------------------|
#                   GNU LESSER GENERAL PUBLIC LICENSE                          |
#                 ------------------------------------                         |
# This source file is free software; you can redistribute it and/or modify it  |
# under the terms of the GNU Lesser General Public License as published by the |
# Free Software Foundation; either version 2.1 of the License, or (at your     |
# option) any later version. This source is distributed in the hope that it    |
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warrant   |
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser   |
# General Public License for more details. You should have received a copy of  |
# the GNU Lesser General Public License along with this  source; if not,       |
# download it from http://www.gnu.org/licenses/lgpl-2.1.html                   |
#------------------------------------------------------------------------------|

import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BCM)

WRLEN = [17, 27, 22]    #Pines de conexion de los reles de las WR-LEN
GPIO.setwarnings(False)

try:
        GPIO.setup(WRLEN[0], GPIO.OUT)
        GPIO.setup(WRLEN[1], GPIO.OUT)
        GPIO.setup(WRLEN[2], GPIO.OUT)
except Exception as e:
        print e

def apaga(len):
        GPIO.output(len, GPIO.LOW)
        #print 'Off',len

def enciende(len):
        GPIO.output(len, GPIO.HIGH)
        #print "On", len

if __name__ == "__main__":
        if len(sys.argv) > 2:
                if str(sys.argv[2]) == 'on':
                        try:
                                enciende(int(sys.argv[1]))
                        except Exception as e:
                                print e

                elif str(sys.argv[2]) == 'off':
                        try:
                                apaga(int(sys.argv[1]))
                        except Exception as e:
                                print e

        else:
                print "usage: python gpi.py <number> <status>"
                print
                print "where:"
                print "\t -number is 17 or 22 or 27"
                print "\t -status on or off"
