#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

class AdvertsTable:

    def __init__(self):
        self._data = []

    # TODO: redefine [x,y] operator (as in numpy)
    def get_data(self, row_index, column_index):
        return self._data[row_index][column_index]

    # TODO: redefine [x,y] operator (as in numpy)
    def set_data(self, row_index, column_index, value):
        if not isinstance(value, self.dtype[column_index]):
            raise ValueError("Expect {} instance. Got {}".format(type(self.dtype[column_index]), type(value)))
        self._data[row_index][column_index] = value

    def append(self, row):
        row_index = self.num_rows - 1
        self.insert_empty_row(row_index)
        for column_index in range(self.num_columns):
            self.set_data(row_index, column_index, row[column_index])

    def insert_empty_row(self, index):
        new_row = list(self.default_values)
        self._data.insert(index, new_row)

    def remove_row(self, index):
        if self.num_rows > 0:
            _removed = self._data.pop(index)

    @property
    def num_rows(self):
        return len(self._data)

    @property
    def num_columns(self):
        return len(self.headers)

    @property
    def shape(self):
        return (self.num_rows, self.num_columns)

    @property
    def headers(self):
        return ("Date",
                "Score",
                "Category",
                "Organization",
                "Title",
                "URL",
                "Pros",
                "Cons",
                "Description")

    @property
    def default_values(self):
        return (datetime.datetime.now(),
                int(0),
                self.category_list[0],
                "",
                "",
                "",
                "",
                "",
                "")

    @property
    def dtype(self):
        return (datetime.datetime, int, str, str, str, str, str, str, str)

    @property
    def category_list(self):
        return ("Entrprise", "IR/IE", "PostDoc")
