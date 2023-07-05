# -*- coding: utf-8 -*-
"""
Created on Thu May 11 22:21:04 2023

@author: japha
"""

import gravpy as gpy
import numpy as np

profile = gpy.gravityProfile()
profile.importdata('PFOax_GRAV.xlsx', sheet_name=1, usecols=[0, 1, 6, 9, 12],
                   parse_dates=[['DATE', 'TIME']])

print(profile.database.info())
print(profile.database.head())

profile.setStations('ESTACION')
profile.groupStations()
print(profile.stations)

profile.setData('GRAV')
print(profile.gravity)

profile.setDate('DATE_TIME')
print(profile.date)
print(profile.time)

print(profile.database)

profile.plot_profile()