#!/usr/bin/python3
# coding: utf8
'''
Application to check some parameters returned by stat command of WR-Core

@file
@author Felipe Torres González<felipetg@ugr.es>
@date January 20, 2016
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

import re
import argparse as arg

# Get servo state
SS_REGEX   = 'ss:\'(\w+)\''
TEMP_REGEX = '\d{1,3}\.\d{4}'


class Log_Checker():
    '''
    This class checks some parameters in the output from stat command of the WRC
    '''

    def __init__(self, filein):
        '''
        Constructor

        Args:
            filein (file) : Input file with the output from stat
        '''
        try:
            self.log = open(filein, 'r')
        except Exception as e:
            print("The file %s could not be opened" % filein)
            raise e

        self.ss_regex = re.compile(SS_REGEX)
        self.temp_regex = re.compile(TEMP_REGEX)

    def check_sync(self, state="TRACK_PHASE"):
        '''
        Method to check the servo state (sync status)

        Args:
            state (str) : The expected state

        Returns:
            How many times sync is lost
        '''
        sync_lost = 0
        line = self.log.readline()
        ss = ""

        while (line != ""):
            servostate = self.ss_regex.search(line)
            if servostate is not None:
                ss = servostate.group(1)
            if ss != state and servostate is not None:
                print(line)
                sync_lost += 1
            line = self.log.readline()

        return sync_lost

    def check_temp(self, min, max):
        '''
        Method to check the temperature of the board

        Args:
            min (int) : Minimal value allowed
            max (int) : Maximum value allowed

        Returns:
            How many times temp is out of range
        '''
        line = self.log.readline()
        temp_out = 0
        t = "0"

        while (line != ""):
            temp = self.temp_regex.search(line)
            if temp is not None:
                t = temp.group(0)
            if not (min < float(t) < max) and temp is not None:
                print("Temp out of range : %s" % t)
                temp_out += 1
            line = self.log.readline()

        return temp_out


def main():
    parser = arg.ArgumentParser("WR LOG Checker")

    parser.add_argument('INPUT', metavar='input', help='Input LOG file')
    parser.add_argument('-s','--sync', help=("Check sync"),default=False, \
    action="store_true")
    parser.add_argument('-t','--temp', help=("Check temp range [min,max]"), \
    nargs='+',type=float)

    args = parser.parse_args()

    lc = Log_Checker(args.INPUT)
    sync_failures = 0
    temp_failures = 0
    if args.sync:
        sync_failures = lc.check_sync()
        if not sync_failures:
            print("The WR synchronization is OK")
        else:
            print("WR sync have been lost (%d) times" % sync_failures)
    if len(args.temp) == 2:
        temp_failures = lc.check_temp(args.temp[0],args.temp[1])
        if not temp_failures:
            print("The temperature was in range")
        else:
            print("Temperature was out of range %d times" % temp_failures)

    return (sync_failures+temp_failures)

if __name__ == '__main__':
    main()
