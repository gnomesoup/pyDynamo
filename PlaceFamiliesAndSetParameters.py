import clr
import sys

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
app = doc.Application

# The inputs to this node will be stored as a list in the IN variables.
familySymbols = UnwrapElement(IN[0])
placementPoints = IN[1]
parameterNames = IN[2]
parameterValues = IN[3]
view = UnwrapElement(IN[4])

outList = []
# parameterNames = ["Group Sort", "Key Value", "Note", "Group"]

TransactionManager.Instance.EnsureInTransaction(doc)

for familySymbol, placementPoint, lineValues in zip(familySymbols, placementPoints, parameterValues):
    location = XYZ(placementPoint.X, placementPoint.Y, placementPoint.Z)
    element = doc.Create.NewFamilyInstance(location, familySymbol, view)
    pList = []
    try:
        for parameterName, value in zip(parameterNames, lineValues):
            parameter = element.LookupParameter(parameterName)
            if not isinstance(value, str):
                value = str(value)
            parameter.Set(value)
            pList.append(parameterName + ":" + value)
        outList.append(element)
    except Exception as e:
        outList.append(e)

TransactionManager.Instance.TransactionTaskDone()

# Assign your output to the OUT variable.
OUT = outList
