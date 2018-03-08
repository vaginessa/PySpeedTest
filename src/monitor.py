# -*- coding: utf-8 -*-
"""
This is the main file that should be run to continously monitor internet
speed tests.
"""

import argparse

parser = argparse.ArgumentParser(description=
                                 "Run continous internet speed tests.")
parser.add_argument('-o',
                    default='speed_record.ilog',
                    help="name of the file to write to",
                    metavar="filename",
                    dest='REC_FILE')
parser.add_argument('-l', '--location',
                    default='No location',
                    help="where the testing is taking place",
                    metavar="location",
                    dest='LOCATION')
parser.add_argument('-f', '--freq',
                    default=0.5,
                    type=float,
                    help="frequency of testing, in minutes",
                    metavar="frequency",
                    dest='FREQ')
parser.add_argument('-v',
                    default=0,
                    type=int,
                    help="verbosity level.  [1, 3]",
                    metavar="verbosity",
                    dest='VERBOSITY')
parser.add_argument('-s', '--server',
                    default='',
                    help="optionally specify a testing server",
                    metavar='server',
                    dest='FORCE_SERVER')
args = parser.parse_args()
