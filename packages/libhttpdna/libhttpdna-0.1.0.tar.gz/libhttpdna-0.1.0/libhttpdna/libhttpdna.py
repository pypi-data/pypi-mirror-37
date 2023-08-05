#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 16:09:37 2018

@author: antony
"""

import libdna

def get_loc_from_params(id_map):
    chr = id_map['chr'][0]
    start = id_map['s'][0]
    end = id_map['e'][0]
    
    if start > end:
      start = start ^ end
      end = start ^ end
      start = start ^ end
    
    return libdna.Loc(chr, start, end)
