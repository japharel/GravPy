# -*- coding: utf-8 -*-
"""
Created on Thu May 11 21:34:38 2023

@author: japha
"""
# TODO
# TIDE CORRECTION AND TIDE SETTER

# GravPy: Gravity data correction and visualization module

# Libraries and modules
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Gravity super-class
class gravityData:
    """
    Gravity super-class for setting data and general corrections
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

    # SETTERS
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

        if file_ext == '.csv' or file_ext == '.txt':
            self.database = pd.read_csv(filename, **kwargs)

        elif file_ext == '.xlsx':
            self.database = pd.read_excel(filename, **kwargs)
        else:
            raise TypeError('Can only read .csv, .txt or .xlsx files')

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
        try:
            self.database.rename(columns={colname: 'gravity'}, inplace=True)
        except Exception as e:
            print('An error occured:', str(e))
        else:
            self.gravity = self.database['gravity']

    def setTime(self, colname=None):
        """
        Assign the measurement times given a column name in the file read

        Parameters
        ----------
        colname : str, optional
            Name of the column which contains the measurement times.
            The default is None.

        Returns
        -------
        None.

        """
        try:
            self.database.rename(columns={colname: 'time'}, inplace=True)
        except Exception as e:
            print('An error occured:', str(e))
        else:
            self.time = self.database['time']

    def setDate(self, colname=None):
        """
        Assign the measurement dates (including time) given a column
        name in the file read

        Parameters
        ----------
        colname : str, optional
            Name of the column which contains the measurement dates.
            The default is None.

        Returns
        -------
        None.

        """
        try:
            self.database['date'] = self.database[colname].dt.date
            self.database['time'] = self.database[colname].dt.time
        except Exception as e:
            print('An error occured:', str(e))
        else:
            self.date = self.database['date']
            self.time = self.database['time']
            self.database.drop(columns=[colname], inplace=True)

    def setBase(self, name=None, coord=None, utm=False):
        """
        Sets the base station's name and latitude or northing coordinate

        Parameters
        ----------
        name : str, optional
            Name of the station. The default is None.
        coord : float, optional
            Coordinate of the station. If utm is True,
            value provided should be in meters. The default is None.
        utm : bool, optional
            If True, coordinate of the station is considered to be in UTM.
            The default is False.

        Returns
        -------
        None.

        """
        try:
            self.baseName = name
        except Exception as e:
            print('An error occured:', str(e))

        try:
            if utm:
                self.baseNorthing = coord
            else:
                self.baseLatitude = coord
        except Exception as e:
            print('An error occured:', str(e))

    def setStationCoords(self, colnames=None, utm=False):
        """
        Sets coordinates of the stations, either in degrees or meters (UTM).

        Parameters
        ----------
        colnames : list, optional
            List or tuple containing the column names of the
            stations' coordinates. If utm is True, column order
            should be (easting, northing); else, column order should
            be (latitude, longitude). The default is None.
        utm : bool, optional
            If True, coordinates are considered to be in UTM.
            The default is False.

        Returns
        -------
        None.

        """
        if utm:
            try:
                self.database.rename(columns={colnames[0]: 'easting', colnames[1]: 'northing'})
            except Exception as e:
                print('An error occured:', str(e))
            else:
                self.easting = self.database['easting']
                self.northing = self.database['northing']
        else:
            try:
                self.database.rename(columns={colnames[0]: 'latitude', colnames[1]: 'longitude'})
            except Exception as e:
                print('An error ocurred:', str(e))
            else:
                self.latitude = self.database['latitude']
                self.longitude = self.database['longitude']

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
        try:
            self.database.rename(columns={colname: 'stations'}, inplace=True)
        except Exception as e:
            print('An error occured:', str(e))
        else:
            self.stations = self.database['stations']

    def setElevation(self, colname=None):
        """
        Sets the elevation values from the database column

        Parameters
        ----------
        colname : str, optional
            Name of the column containing elevation values.
            The default is None.

        Returns
        -------
        None.

        """
        try:
            self.database.rename(columns={colname: 'elevation'}, inplace=True)
        except Exception as e:
            print('An error occured:', str(e))
        else:
            self.elevation = self.database['elevation']

    # METHODS
    def groupStations(self):
        """
        Groups stations in database by name, averaging all values
        and assigning it back to the database

        Returns
        -------
        None.

        """

        self.database = self.database.groupby(self.stations, as_index=False, sort=False).mean()
        self.stations = self.database['stations']

    def lat_dist(self, distance):
        """
        Converts the distance of the stations to the base from
        meters to degrees, using the base's latitude.

        Parameters
        ----------
        distance : array_like
            Distances of the stations to the base, in meters.

        Raises
        ------
        RuntimeError
            Raised when user has not set stations' or base's coordinates.

        Returns
        -------
        deg_dist : array_like
            Distances converted to degrees.

        """
        if hasattr(self, 'latitude') and hasattr(self, 'baseLatitude'):
            deg_2_m = 111 * 10e2
            if hasattr(self, 'baseNorthing'):
                st_m = distance + self.baseNorthing
            else:
                base_m = self.baseLatitude * deg_2_m
                st_m = distance + base_m
        else:
            raise RuntimeError('No latitudes were assigned to the stations or to the base')

        deg_dist = st_m / deg_2_m

        return deg_dist

    def gn(self):
        """
        Calculates the normal gravity for a given latitude using
        the GRS 1967 equation for the theoretical gravity
        (in miligals).

        Raises
        ------
        RuntimeError
            Raised when no values for the stations' latitude
            has been set yet.

        Returns
        -------
        gn_eq : array_like
            Returns the calculated normal gravity at the stations,
            using the provided latitude.

        """
        if hasattr(self, 'latitude'):
            rad_lat = np.deg2rad(self.latitude)
            gn_eq = 978031.846 * (1 + 0.0053024 * np.sin(rad_lat)**2 -
                                  0.0000058 * np.sin(2 * rad_lat))
            return gn_eq
        else:
            raise RuntimeError('No value for the latitudes has been set yet')


    def drift_correction(self):
        """
        Calculates the drift correction for gravity data, given
        the base and readings taken at each station

        Raises
        ------
        RuntimeError
            Raised only when gravity values have no been set.

        Returns
        -------
        drift_corr : array_like
            Drift correction values for each station.

        """

        # Creating the array to allocate the values
        if not hasattr(self, 'gravity'):
            raise RuntimeError('Gravity data has not been set yet')

        drift_corr = np.zeros(self.gravity.size)

        bases = self.database[self.database['stations'].str.contains(self.baseName)]

        old_grav = bases['gravity'].iloc[0]
        old_time = bases['time'].iloc[0]
        new_grav = bases['gravity'].iloc[1]
        new_time = bases['time'].iloc[1]

        for i in range(drift_corr.size):
            if self.stations[i] in bases['stations'] and self.stations[i] != self.baseName:
                old_grav = new_grav
                old_time = new_time

                new_base = bases[bases['stations'] == self.stations[i]]
                new_grav = new_base['gravity']
                new_time = new_base['time']

            drift_corr[i] = ((new_grav - old_grav) / (new_time - old_time)) * (self.time[i] - old_time)

        return drift_corr

    def relative_g(self):
        """
        Calculates relative gravity

        Returns
        -------
        relative_gravity : array_like
            Values of the calculated relative gravity.

        """
        relative_gravity = self.gravity - self.gravity[0]

        return relative_gravity

    def latitude_correction(self, distance):
        """
        Calculates the latitude correction for gravtity data

        Parameters
        ----------
        distance : array_like
            Distances from the station to the base.

        Raises
        ------
        RuntimeError
            Raised only when no values for the latitude or the base have been provided.

        Returns
        -------
        lat_corr : array_like
            Latitude correction values for each station.

        """

        if not hasattr(self, 'latitude') or (not hasattr(self, 'baseLatitude')
                                             and not hasattr(self, 'baseNorthing')):
            raise RuntimeError('No values for the latitude of the stations or base have been given')

        if distance is None:
            if hasattr(self, 'baseNorthing') and hasattr(self, 'northing'):
                distance = self.northing - self.baseNorthing
            else:
                r = 6367.44
                dl = self.latitude - self.baseLatitude
                distance = r * dl

        rad_baseLat = np.deg2rad(self.baseLatitude)
        lat_corr = 0.811 * np.sin(2 * rad_baseLat) * distance

        return lat_corr

    def air_correction(self):
        """
        Calculates the air correction for gravtity data

        Returns
        -------
        air_corr : array_like
            Air correction values for each station.

        """
        air_corr = -0.3086 * self.elevation

        return air_corr

    def bouguer_correction(self, rho=2.67):
        """


        Parameters
        ----------
        rho : float, optional
            Density value used for the Bouger slab, in [g/cm3].
            The default is 2.67 [g/cm3].

        Returns
        -------
        boug_corr : array_like
            Bouguer correction for each station.

        """
        boug_corr = 0.04192 * rho * self.elevation

        return boug_corr

# 1d gravity profile
class gravityProfile(gravityData):

    def plot_profile(self, ax=None, **kwargs):
        if ax is None:
            fig, ax = plt.subplots()

        ax.plot(self.stations, self.gravity, **kwargs)

# 2d gravity map
class gravityMap(gravityData):

    def plot_map(self, ax=None, **kwargs):
        if ax is None:
            fig, ax = plt.subplots()

        ax.scatter(self.easting, self.northing, c=self.gravity, **kwargs)