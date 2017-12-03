# -*- coding: utf-8 -*-
# !/usr/bin/env python3


from PyQt5.QtCore import *
##----------------------------------------------------------------------------
class Porperties(object):

    def __init__(self):

        self._values = QVariantMap()

    #-------------------------------------------------------------------------
    def put(self, name, v):

        self._values.insert(name, v)

        # //if (!result.second)
        # //std::cout << "Properties already have a value with the name '"
        # //<< name.toLocal8Bit().data()
        # //<< "'"
        # //<< std::endl;

    #-------------------------------------------------------------------------
    def get(self, name, v):

        var = self._values[name]

        if(var.canConver()):

            v = self._values[name].value()

            return True

        return False

    #-------------------------------------------------------------------------
    def values(self):

        return self._values

##----------------------------------------------------------------------------

