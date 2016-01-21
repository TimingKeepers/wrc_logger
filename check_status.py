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
SS_REGEX   = 'ss:\'(\w*)\''
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
            self.file = self.log.readlines()
            self.log.close()
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
        ss = ""

        for line in self.file:
            servostate = self.ss_regex.search(line)
            if servostate is not None:
                if servostate.group(1) != state:
                    sync_lost += 1

        return sync_lost

    def check_temp(self, min, max, verbose=False):
        '''
        Method to check the temperature of the board

        Args:
            min (int) : Minimal value allowed
            max (int) : Maximum value allowed
            verbose (bool) : Adds to the returned value the mean temperature

        Returns:
            How many times temp is out of range
        '''
        temp_out = 0
        t = "0"
        m_t = 0
        i = 0

        for line in self.file:
            temp = self.temp_regex.search(line)
            if temp is not None:
                t = temp.group(0)
                m_t += float(t)
                i += 1
            if not (min < float(t) < max) and temp is not None:
                temp_out += 1

        return (temp_out,) if not verbose else (temp_out, m_t/i)


def main():
    parser = arg.ArgumentParser("WR LOG Checker")

    parser.add_argument('INPUT', metavar='input', help='Input LOG file')
    parser.add_argument('-s','--sync', help=("Check sync"),default=False, \
    action="store_true")
    parser.add_argument('-t','--temp', help=("Check temp range [min,max]"), \
    nargs='?',type=str)
    parser.add_argument('-v','--verbose', help=("Enable verbose mode"), \
    action="store_true", default=False)

    args = parser.parse_args()

    lc = Log_Checker(args.INPUT)
    sync_failures = 0
    temp_failures = 0
    if args.sync:
        sync_failures = lc.check_sync()
        if not sync_failures:
            print("The WR synchronization is OK")
        else:
            print("WR sync is lost")
    if args.temp is not None:
        temp = [float(i) for i in args.temp.split(",")]
        if len(temp) >= 2:
            temp_failures = lc.check_temp(temp[0], temp[1], args.verbose)
            if not temp_failures[0] and not args.verbose:
                print("The temperature was in range")
            elif not temp_failures[0] and args.verbose:
                print("The temperature was in range : %f" % (temp_failures[1]))
            else:
                print("Temperature was out of range:")
                if args.verbose:
                    print("Mean temperature : %.2f ºC (range=[%.2f,%.2f])" % \
                    (temp_failures[1],temp[0],temp[1]))
        else: print("Error: Temp checking needs 2 parameters: min, max")

    return (sync_failures+temp_failures[0])

if __name__ == '__main__':
    main()
