#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SwissHydroData enables you to fetch data
from the Federal Office for the Environment FOEN
"""

from datetime import datetime
import requests


class SwissHydroData:
    """
    SwissHydroData enables you to fetch data from
    the Federal Office for the Environment FOEN
    """

    def __init__(self):
        self.base_url = 'https://swisshydroapi.bouni.de/api/v1'

    def get_stations(self):
        """ Return a list of all stations IDs """
        request = requests.get("{}/stations".format(
            self.base_url))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station(self, station_id):
        """ Return all data for a given station """
        request = requests.get("{}/station/{}".format(
            self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_name(self, station_id):
        """ Return name for a given station """
        request = requests.get("{}/station/{}/name".format(
            self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_water_body_name(self, station_id):
        """ Return water body name for a given station """
        request = requests.get("{}/station/{}/water-body-name".format(
            self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_water_body_type(self, station_id):
        """ Return water body type for a given station """
        request = requests.get("{}/station/{}/water-body-type".format(
            self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_coordinates(self, station_id):
        """ Return WSG84 coordinates for a given station """
        request = requests.get("{}/station/{}/coordinates".format(
            self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_parameters(self, station_id):
        """ Return measurement data for a given station """
        request = requests.get("{}/station/{}/parameters".format(
            self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_temperature(self, station_id):
        """ Return temperature data for a given station """
        request = requests.get("{}/station/{}/parameters/temperature".format(
            self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_temperature_unit(self, station_id):
        """ Return temperature unit for a given station """
        request = requests.get(
            "{}/station/{}/parameters/temperature/unit".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_temperature_datetime(self, station_id):
        """ Return temperature measurement datetime for a given station """
        request = requests.get(
            "{}/station/{}/parameters/temperature/datetime".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return datetime.strptime(request.json(), "%Y-%m-%dT%H:%M:%S")

    def get_station_temperature_value(self, station_id):
        """ Return temperature value for a given station """
        request = requests.get(
            "{}/station/{}/parameters/temperature/value".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_temperature_previous24h(self, station_id):
        """ Return temperature value 24h ago for a given station """
        request = requests.get(
            "{}/station/{}/parameters/temperature/previous24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_temperature_delta24h(self, station_id):
        """ Return temperature delta of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/temperature/delta24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_temperature_max24h(self, station_id):
        """ Return temperature maximum of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/temperature/max24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_temperature_mean24h(self, station_id):
        """ Return temperature mean of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/temperature/mean24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_temperature_min24h(self, station_id):
        """ Return temperature minimum of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/temperature/min24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_temperature_max1h(self, station_id):
        """ Return temperature maximum of the last hour for a given station """
        request = requests.get(
            "{}/station/{}/parameters/temperature/max1h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_temperature_mean1h(self, station_id):
        """ Return temperature mean of the last hour for a given station """
        request = requests.get(
            "{}/station/{}/parameters/temperature/mean1h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_temperature_min1h(self, station_id):
        """ Return temperature minimum of the last hour for a given station """
        request = requests.get(
            "{}/station/{}/parameters/temperature/min1h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_level(self, station_id):
        """ Return water level measurement for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_level_unit(self, station_id):
        """ Return water level unit for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level/unit".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_level_datetime(self, station_id):
        """ Return water level measurement datetime for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level/datetime".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return datetime.strptime(request.json(), "%Y-%m-%dT%H:%M:%S")

    def get_station_level_value(self, station_id):
        """ Return water level value for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level/value".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_level_previous24h(self, station_id):
        """ Return water level 24h ago for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level/previous24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_level_delta24h(self, station_id):
        """ Return water level delta of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level/delta24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_level_max24h(self, station_id):
        """ Return water level maximum of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level/max24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_level_mean24h(self, station_id):
        """ Return water level mean of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level/mean24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_level_min24h(self, station_id):
        """ Return water level minimum of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level/min24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_level_max1h(self, station_id):
        """ Return water level maximum of the last hour for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level/max1h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_level_mean1h(self, station_id):
        """ Return water level mean of the last hour for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level/mean1h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_level_min1h(self, station_id):
        """ Return water level minimum of the last hour for a given station """
        request = requests.get(
            "{}/station/{}/parameters/level/min1h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_discharge(self, station_id):
        """ Return discharge measurement for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_discharge_unit(self, station_id):
        """ Return discharge unit for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge/unit".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_discharge_datetime(self, station_id):
        """ Return discharge measurement datetime for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge/datetime".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return datetime.strptime(request.json(), "%Y-%m-%dT%H:%M:%S")

    def get_station_discharge_value(self, station_id):
        """ Return discharge value for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge/value".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_discharge_previous24h(self, station_id):
        """ Return discharge 24h ago for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge/previous24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_discharge_delta24h(self, station_id):
        """ Return discharge delta of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge/delta24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_discharge_max24h(self, station_id):
        """ Return discharge maximum of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge/max24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_discharge_mean24h(self, station_id):
        """ Return discharge mean of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge/mean24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_discharge_min24h(self, station_id):
        """ Return discharge minimum of the last 24h for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge/min24h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_discharge_max1h(self, station_id):
        """ Return discharge maximum of the last hour for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge/max1h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_discharge_mean1h(self, station_id):
        """ Return discharge mean of the last hour for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge/mean1h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()

    def get_station_discharge_min1h(self, station_id):
        """ Return discharge minimum of the last hour for a given station """
        request = requests.get(
            "{}/station/{}/parameters/discharge/min1h".format(
                self.base_url, station_id))
        if request.status_code != 200:
            return None
        return request.json()
