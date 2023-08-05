#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import datetime
import json
import os

from jhunt.data.adverts import AdvertsTable
from jhunt.io.lock import lock_path, unlock_path

PY_DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

FILE_NAME = ".jhunt_adverts"

class AdvertsDataBase:

    def __init__(self):
        lock_path(self.path)


    def __del__(self):
        unlock_path(self.path)


    def load(self):
        """Load the JSON database."""

        json_data = []

        try:
            with open(self.path, "r") as fd:
                json_data = json.load(fd)
        except FileNotFoundError:
            pass

        for row in json_data:
            row[0] = datetime.datetime.strptime(row[0], PY_DATE_TIME_FORMAT)

        data = AdvertsTable()
        for row in json_data:
            data.append(row)

        return data


    def save(self, data):
        """Save the JSON database."""

        json_data = copy.deepcopy(data._data)          # TODO !!! get each row from it's public interface

        for row in json_data:
            row[0] = row[0].strftime(format=PY_DATE_TIME_FORMAT)

        with open(self.path, "w") as fd:
            #json.dump(json_data, fd)                           # no pretty print
            json.dump(json_data, fd, sort_keys=True, indent=4)  # pretty print format


    @property
    def path(self):
        home_path = os.path.expanduser("~")                 # TODO: works on Unix only ?
        file_path = os.path.join(home_path, FILE_NAME)
        return file_path
