# -*- coding: utf-8 -*-
"""
Created on Thu May 11 22:21:04 2023

@author: japha
"""

import gravpy as gpy

profile = gpy.gravityProfile()
profile.importdata('grav_csv_test.csv',
                   usecols=['Station', 'NAD83_E','NAD83_N',
                            'NAVD88','Obs_grav'])

print(profile.database)