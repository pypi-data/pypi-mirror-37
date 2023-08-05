#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from jhunt.io.adverts import AdvertsDataBase
from jhunt.qt.widgets.mainwindow import MainWindow

from PyQt5.QtWidgets import QApplication

APPLICATION_NAME = "JHunt"


def main():

    advert_database = AdvertsDataBase()
    data = advert_database.load()              # TODO ?

    app = QApplication(sys.argv)
    app.setApplicationName(APPLICATION_NAME)

    # Make widgets
    window = MainWindow(data)

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    advert_database.save(data)              # TODO ?

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
