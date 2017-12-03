# -*- coding: utf-8 -*-
# !/usr/bin/env python3

#from typing import *
from abc import abstractmethod

#from sip import wrappertype

class Serializable(object):

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def restore(self,  jsonObject):
        pass



###############################################################################

    
