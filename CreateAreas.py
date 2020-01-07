import clr

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Imports Ilists module into python
clr.AddReference("System")
from System.Collections.Generic import List as cList

# Standard areas for Current Document, Active UI and application
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

if not isinstance(IN[0], list):
    names = [IN[0]]
else:
    names = IN[0]
names = UnwrapElement(names)

if not isinstance(IN[0], list):
    numbers = [IN[0]]
else:
    numbers = IN[0]
numbers = UnwrapElement(numbers)

if not isinstance(IN[1], list):
    locations = [IN[1]]
else:
    locations = IN[1]
locations = UnwrapElement(locations)

if not isinstance(IN[2], list):
    views = [IN[2]]
else:
    views = IN[2]
views = UnwrapElement(views)

outList = []

def toXYZ(fPoint):
    return XYZ(fPoint.X, fPoint.Y, fPoint.Z)

view = views[0]

TransactionManager.Instance.EnsureInTransaction(doc)

for name, number, location in zip(names, numbers, locations):
    try:
        area = doc.Create.NewArea(view, UV(location.X, location.Y))
        area.Name = name
        area.Number = number
        outList.append(area)
    except Exception, exception:
        outList.append(exception)

TransactionManager.Instance.TransactionTaskDone()

OUT = outList
