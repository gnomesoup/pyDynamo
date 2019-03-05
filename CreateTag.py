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
elements = UnwrapElement(IN[0])
placementPoints = UnwrapElement(IN[1])
# view = UnwrapElement(IN[0])

outList = []
# parameterNames = ["Group Sort", "Key Value", "Note", "Group"]

TransactionManager.Instance.EnsureInTransaction(doc)

for element, placementPoint in zip(elements, placementPoints):
    tag = doc.Create.NewTag(doc.ActiveView, element, False, TagMode.TM_ADDBY_MATERIAL,
                      TagOrientation.Horizontal, XYZ(placementPoint.X, placementPoint.Y, 0))
    outList.append(tag)

TransactionManager.Instance.TransactionTaskDone()

# Assign your output to the OUT variable.
OUT = outList
