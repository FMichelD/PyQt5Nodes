# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from enum import Enum

#-----------------------------------------------------------------------------
class PortType(Enum):
    No_One = 0
    In = 1
    Out = 2

#-----------------------------------------------------------------------------
PortIndex = int

INVALID = -1

#-----------------------------------------------------------------------------
class Port(object):

    def __init__(self, typePort: PortType=PortType.No_One, index: PortIndex=INVALID):

        self.type = typePort

        self.index  = index


    #--------------------------------------------------------------------------
    def indexIsValid(self) -> bool:
        return (self.index != INVALID)

    #--------------------------------------------------------------------------
    def portTypeIsValid(self) -> bool:
        return (self.type != PortType.No_One)


##----------------------------------------------------------------------------
def oppositePort(port: PortType) -> PortType:

    result = PortType.No_One

    if(port == PortType.In):
        result = PortType.Out

    elif(port == PortType.Out):
        result = PortType.In

    return result

#-----------------------------------------------------------------------------
