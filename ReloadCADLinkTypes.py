# Only for 2018 and greater
# http://www.revitapidocs.com/2018/41db0b8b-4bd4-02b0-f06a-a7a169802e1b.htm

import clr
import sys
from System.IO import Directory, Path, File

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

def reload(cad, path):
    try:
        if (path and File.Exists(path)):
            cad.ReloadFrom(path)
            return True
        else:
            cad.Reload()
            return True
    except:
        return False

outList

cadLinks = IN[0]
if not isinstance(cadLinks, list):
    cadLinks = [cadLinks]

paths = IN[1]
if not isinstance(paths, list):
    paths = [paths]

for link, path in zip(cadLinks, paths):
    outList.append(reload(link, path))

OUT = outList
