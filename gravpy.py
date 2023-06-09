# -*- coding: utf-8 -*-
"""
Created on Thu May 11 21:34:38 2023

@author: japha
"""

# GravPy: Gravity correction and visualization module

# Libraries and modules
import os

import numpy as np
import pandas as pd

# 1D gravity class
class gravityProfile:
    """
    Gravity profile data processing and visualization (1D profiles)
    """

    def __init__(self, filename=None):
        """
        Initialization of the gravityProfile object. Initialization can be
        empty or with a provided filename for the gravity data.

        Parameters
        ----------
        filename : str, optional
            The data file name. Supported formats are .xlsx and .csv.
            The default is None.

        Returns
        -------
        None.

        """

        if filename is not None:
            self.importdata(filename)

    def importdata(self, filename, **kwargs):
        """
        Import the file data containing the gravity profile

        Parameters
        ----------
        filename : str
            Name of the .csv or .xlsx file to be imported.
        **kwargs
            Additional arguments for read_csv() and read_excel() functions.

        Raises
        ------
        TypeError
            If input file extension does not belong to accepted types.

        Returns
        -------
        None.

        """

        file_name, file_ext = os.path.splitext(filename)

        if file_ext == '.csv':
            self.database = pd.read_csv(filename, **kwargs)

        elif file_ext == '.xlsx':
            self.database = pd.read_excel(filename, **kwargs)

        else:
            raise TypeError('Can only read .csv or .xlsx files')

    def setData(self, colname=None):
        """
        Assign the gravity data given a column name in the file read

        Parameters
        ----------
        colname : str, optional
            Name of the column which contains the measured gravity values.
            The default is None.

        Returns
        -------
        None.

        """
        if colname:
            self.gravity = self.database[colname]
        else:
            print('Please provide a column name containing gravity data')

    def setTime(self, colname=None, dec=False):
        """
        Assign the measurement times given a column name in the file read

        Parameters
        ----------
        colname : str, optional
            Name of the column which contains the measurement times.
            The default is None.
        dec : bool, optional
            True if the input time is in decimal format.
            The default is False.

        Returns
        -------
        None.

        """

        if colname:
            self.time = self.database[colname]
        else:
            print('Please provide a column name containing times')

        self.decimal = dec

    def setDate(self, colname=None, dec=False):
        """
        Assign the measurement dates (including time) given a column
        name in the file read

        Parameters
        ----------
        colname : str, optional
            Name of the column which contains the measurement dates.
            The default is None.
        dec : bool, optional
            True if the input time is in decimal format.
            The default is False.

        Returns
        -------
        None.

        """
        if colname:
            self.date = self.database[colname]
        else:
            print('Please provide a column name containing dates')

        self.decimal = dec

    def setBaseLat(self, latitude=None):
        """
        Assign the base latitude given an input value

        Parameters
        ----------
        latitude : float, optional
            Latitude of the profile's base. The default is None.

        Returns
        -------
        None.

        """
        if latitude:
            self.baseLatitude = latitude
        else:
            print('Please specify a latitude')

    def setStationLatitude(self, colname=None):
        if colname:
            self.stationLatitude = self.database[colname]
        else:
            print('Please provide a column name containing latitudes')

    def setStations(self, colname=None):
        """
        Assigns the stations names given a column name in the file read

        Parameters
        ----------
        colname : str, optional
            Names of the stations.
            The default is None.

        Returns
        -------
        None.

        """
        if colname:
            self.stations = self.database[colname]
        else:
            print('Please provide a column name containing station names')


    def hms_to_hh(self, date):
        """
        Converts hours in HH:MM:SS to HH.hh format

        Parameters
        ----------
        date : array_like
            Dates, including times, of the measurements.

        Returns
        -------
        hh_time : TYPE
            Converted times to decimal time.

        """

        hh_time = np.array([t.hour + t.minute / 60 + t.second / 3600 for t in date])

        return hh_time

# TODO
    def groupStations():
        pass


# # Functions for gravity data corrections

# def lat_dist(lat_base, distance):
#     """
#     Converts the distance of the stations from meters to degrees, using the base's latitude.

#     Parameters
#     ----------
#     lat_base : int or float
#                Value of the latitude of the base (in degrees)

#     distance : array_like
#                Contains the distances from the base to the stations (in meters)

#     Returns
#     -------
#     l : array_like
#     """

#     # Factor for conversion from degrees to meters
#     deg_2_m = 111 * 10e2

#     base_m = lat_base * deg_2_m
#     est_m = distance + base_m

#     return est_m / deg_2_m

# def gn(latitude):
#     """
#     Calculates the normal gravity for a given latitude using the GRS 1967 equation for the theoretical gravity (in miligals).

#     Parameters
#     ----------
#     latitude : array_like
#                Contains the latitude of all stations, including the base

#     Returns
#     -------
#     g : array_like
#     """

#     # Conversion from degrees to radians of the latitude
#     latitude = np.deg2rad(latitude)

#     return 978031.846 * (1 + 0.0053024 * np.sin(latitude)**2 - 0.0000058 * np.sin(2 * latitude))

# def drift_correction(time, g_read, station):
#     """
#     Calculates the drift correction for gravity data, given the base and readings taken at each station

#     Parameters
#     ----------
#     time : array_like
#            Contains the time of each reading in HH.hh format

#     g_read : array_like
#                Contains the value of the readings taken at each stations

#     station : array_like
#               Contains the names of each station where the readings were taken, including the base

#     Returns
#     -------
#     g_dc : array_like
#     """

#     # Creating the array to allocate the values
#     g_dc = np.zeros(g_read.size)
#     base_dc = 0

#     # Extracting the array indexes where the name of the base appears
#     idxs = np.where(station == station[0])[0]

#     # Initializing the variables with gravity readings
#     initial_g = g_read[0]
#     final_g = g_read[idxs[1]]
#     initial_t = time[0]
#     final_t = time[idxs[1]]
#     j = 1

#     for i in range(g_dc.size):
#         if i - 1 != 0 and i - 1 in idxs:
#             j += 1
#             initial_g = g_read[i - 1]
#             final_g = g_read[idxs[j]]
#             initial_time = time[i - 1]
#             final_time = time[idxs[j]]
#             base_dc = g_dc[i - 1]
#         g_dc[i] = ((final_g - initial_g) / (final_t - initial_t)) * (time[i] - initial_t) + base_dc

#     return g_dc

# def relative_g(g_obs):
#     """
#     Calculates relative gravity

#     Parameters
#     ----------
#     g_obs : array_like
#                Contains the values of the observed gravity

#     Returns
#     -------
#     g_rel : array_like
#     """

#     g_rel = g_obs - g_obs[0]

#     return g_rel

# def latitude_correction(base_latitude, st_latitude = None, distance = None):
#     """
#     Calculates the latitude correction for gravtity data

#     Parameters
#     ----------
#     base_latitude : int or float
#                     Value of the latitude of the base (in degrees)

#     st_latitude : array_like
#                   Contains the latitude of the stations where the readings were taken (in degrees)

#     distance : array_like
#                Contains the distances of each station from the base

#     Returns
#     -------
#     lat_corr : array_like
#     """

#     if distance is None:
#         r = 6367.44
#         dl = st_latitude - base_latitude
#         dy = r * dl

#         # Conversion from degrees to radians of the base's latitude
#         base_latitude = np.deg2rad(base_latitude)

#         lat_corr = 0.811 * np.sin(2 * base_latitude) * dy
#     else:
#         # Conversion from degrees to radians of the base's latitude
#         base_latitude = np.deg2rad(base_latitude)

#         lat_corr = 0.811 * np.sin(2 * base_latitude) * distance

#     return lat_corr

# def air_correction(h):
#     """
#     Calculates the air correction for gravtity data

#     Parameters
#     ----------
#     h : array_like
#         Contains the height of each station (in meters)

#     Returns
#     -------
#     air_corr : array_like
#     """

#     air_corr = - 0.3086 * h

#     return air_corr

# def bouguer_correction(rho, h):
#     """
#     Calculates the Bouguer correction for gravity data

#     Parameters
#     ----------
#     rho : float
#           Chosen Bouguer's density for the area

#     h : array_like
#         Height of each station (in meters)

#     Returns
#     -------
#     boug_corr : array_like
#     """

#     boug_corr = 0.04192 * rho * h

#     return boug_corr