# -*- coding: utf-8 -*-
"""
Created on Thu May 11 22:21:04 2023

@author: japha
"""

import gravpy as gpy
import numpy as np

profile = gpy.gravityProfile()
profile.importdata('PFOax_GRAV.xlsx', sheet_name=1,
                   parse_dates=[['DATE', 'TIME']], usecols=[0, 1, 6, 9, 10, 12])

profile.setData('GRAV')
profile.setDate('DATE_TIME')