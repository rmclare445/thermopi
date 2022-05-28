#!/usr/bin/env python3

''' 

Uses locator.py to write minimum circle member distance to globally-accessible file
Intended to be run by crontab

'''

import os, locator

api = locator.life360()
if api.authenticate():
    with open("member_distance", "w") as f:
        f.write( str( api.get_min_dist() ) )