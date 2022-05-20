#!/usr/bin/env python3.9
def Spatial(newrow, newtype):
    newrow="%sFromText(%s)" %(newtype,newrow)
    if "FromText(None)" in newrow:
        newrow='""'
    if newtype =="multipolygon":
        newrow= newrow.replace('MULTIPOLYGON','"MULTIPOLYGON').replace(')))',')))"')+','
    elif newtype =="polygon":
        newrow= newrow.replace('POLYGON','"POLYGON').replace('))','))"')+','
    elif newtype =="point":
        newrow= newrow.replace('POINT','"POINT').replace('))',')")')+','
    return newrow