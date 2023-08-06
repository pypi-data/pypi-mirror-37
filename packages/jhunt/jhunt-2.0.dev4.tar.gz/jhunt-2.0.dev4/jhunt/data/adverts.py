#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

class AdvertsTable:

    def __init__(self):
        self._data = []
        self._last_id = 0

    # TODO: redefine [x,y] operator (as in numpy)
    def get_data(self, row_index, column_index):
        return self._data[row_index][column_index]

    # TODO: redefine [x,y] operator (as in numpy)
    def set_data(self, row_index, column_index, value):
        if not isinstance(value, self.dtype[column_index]):
            raise ValueError("Error at row {} column {} with value {}. Expect {} instance. Got {}".format(row_index, column_index, value, self.dtype[column_index], type(value)))

        id_index = self.headers.index("ID")
        if column_index == id_index:
            self._last_id = max(self._last_id, value)

        self._data[row_index][column_index] = value

    def append(self, row):
        row_index = self.num_rows - 1
        self.insert_row(row_index, row=row)

    def insert_row(self, row_index, row=None):
        if row is None:
            row = list(self.default_values)

        self._data.insert(row_index, [None for i in range(self.num_columns)])

        for column_index in range(self.num_columns):
            self.set_data(row_index, column_index, row[column_index])

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
        return ("ID",
                "Date",
                "Score",
                "Application",
                "Category",
                "Organization",
                "Ref.",
                "Title",
                "URL",
                "Pros",
                "Cons",
                "Description")

    @property
    def default_values(self):
        return (int(self._last_id + 1),
                datetime.datetime.now(),
                int(0),
                False,
                self.category_list[0],
                "",
                "",
                "",
                "",
                "",
                "",
                "")

    @property
    def dtype(self):
        return (int,
                datetime.datetime,
                int,
                bool,
                str,
                str,
                str,
                str,
                str,
                str,
                str,
                str)

    @property
    def category_list(self):
        return ("Entreprise", "IR/IE", "PostDoc")
