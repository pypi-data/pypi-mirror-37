#!/usr/bin/env python
#
###############################################################################
#   Copyright (C) 2016  Cortney T. Buffington, N0MJS <n0mjs@me.com>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
###############################################################################

from __future__ import print_function

from os.path import isfile, getmtime
from time import time
from urllib import URLopener
from csv import reader as csv_reader
from csv import DictReader as csv_dict_reader
from binascii import b2a_hex as ahex

# Does anybody read this stuff? There's a PEP somewhere that says I should do this.
__author__     = 'Cortney T. Buffington, N0MJS'
__copyright__  = 'Copyright (c) 2016-2017 Cortney T. Buffington, N0MJS and the K0USY Group'
__credits__    = 'Colin Durbridge, G4EML, Steve Zingman, N4IRS; Mike Zingman'
__license__    = 'GNU GPLv3'
__maintainer__ = 'Cort Buffington, N0MJS'
__email__      = 'n0mjs@me.com'


# CONSTANTS
SUB_FIELDS   = ('ID', 'CALLSIGN', 'NAME', 'CITY', 'STATE', 'COUNTRY', 'TYPE')
PEER_FIELDS  = ('ID', 'CALLSIGN', 'CITY', 'STATE', 'COUNTRY', 'FREQ', 'CC', 'OFFSET', 'TYPE', 'LINKED', 'TRUSTEE', 'INFO', 'OTHER', 'NETWORK', )
TGID_FIELDS  = ('ID', 'NAME')


#************************************************
#     STRING UTILITY FUNCTIONS
#************************************************

# Create a 2 byte hex string from an integer
def hex_str_2(_int_id):
    try:
        return format(_int_id,'x').rjust(4,'0').decode('hex')
    except TypeError:
        raise

# Create a 3 byte hex string from an integer
def hex_str_3(_int_id):
    try:
        return format(_int_id,'x').rjust(6,'0').decode('hex')
    except TypeError:
        raise

# Create a 4 byte hex string from an integer
def hex_str_4(_int_id):
    try:
        return format(_int_id,'x').rjust(8,'0').decode('hex')
    except TypeError:
        raise

# Convert a hex string to an int (radio ID, etc.)
def int_id(_hex_string):
    return int(ahex(_hex_string), 16)


#************************************************
#     ID ALIAS FUNCTIONS
#************************************************

# Download and build dictionaries for mapping number to aliases
# Used by applications. These lookups take time, please do not shove them
# into this file everywhere and send a pull request!!!
# Download a new file if it doesn't exist, or is older than the stale time
def try_download(_path, _file, _url, _stale,):
    now = time()
    url = URLopener()
    file_exists = isfile(_path+_file) == True
    if file_exists:
        file_old = (getmtime(_path+_file) + _stale) < now
    if not file_exists or (file_exists and file_old):
        try:
            url.retrieve(_url, _path+_file)
            result = 'ID ALIAS MAPPER: \'{}\' successfully downloaded'.format(_file)
        except IOError:
            result = 'ID ALIAS MAPPER: \'{}\' could not be downloaded'.format(_file)
    else:
        result = 'ID ALIAS MAPPER: \'{}\' is current, not downloaded'.format(_file)
    url.close()
    return result

# LEGACY VERSION - MAKES A SIMPLE {INTEGER ID: 'CALLSIGN'} DICTIONARY
def mk_id_dict(_path, _file):
    dict = {}
    try:
        with open(_path+_file, 'rU') as _handle:
            ids = csv_reader(_handle, dialect='excel', delimiter=',')
            for row in ids:
                try:
                    dict[int(row[0])] = (row[1])
                except:
                    pass
            _handle.close
            return dict
    except IOError:
        return dict

# NEW VERSION - MAKES A FULL DICTIONARY OF INFORMATION BASED ON TYPE OF ALIAS FILE
# BASED ON DOWNLOADS FROM DMR-MARC, TGID IS STILL A "SIMPLE" DICTIONARY      
def mk_full_id_dict(_path, _file, _type):
    dict = {}
    if _type == 'subscriber':
        fields = SUB_FIELDS
    elif _type == 'peer':
        fields = PEER_FIELDS
    elif _type == 'tgid':
        fields = TGID_FIELDS
    try:
        with open(_path+_file, 'rU') as _handle:
            ids = csv_dict_reader(_handle, fieldnames=fields, restkey='OTHER', dialect='excel', delimiter=',')
            for row in ids:
                for item in row:
                    try:
                        dict[int(row['ID'])] = row
                    except:
                        pass
            _handle.close
            return dict
    except IOError:
        return dict

# THESE ARE THE SAME THING FOR LEGACY PURPOSES
def get_alias(_id, _dict, *args):
    if type(_id) == str:
        _id = int_id(_id)
    if _id in _dict:
        if args:
            retValue = []
            for _item in args:
                try:
                    retValue.append(_dict[_id][_item])
                except TypeError:
                    return _dict[_id]
            return retValue
        else:
            return _dict[_id]
    return _id

def get_info(_id, _dict, *args):
    if type(_id) == str:
        _id = int_id(_id)
    if _id in _dict:
        if args:
            retValue = []
            for _item in args:
                try:
                    retValue.append(_dict[_id][_item])
                except TypeError:
                    return _dict[_id]
            return retValue
        else:
            return _dict[_id]
    return _id
    
    

    
    