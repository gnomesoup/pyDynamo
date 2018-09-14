import clr
import math

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

#selected element
views = IN[0]
if not isinstance(views, list):
    views = [views]
views = UnwrapElement(views)

boundingBoxes = IN[1]
if not isinstance(boundingBoxes, list):
    boundingBoxes = [boundingBoxes]
boundingBoxes = UnwrapElement(boundingBoxes)

outList = []

TransactionManager.Instance.EnsureInTransaction(doc)

for view, boundingBox in zip(views, boundingBoxes):
    try:
        boundingBoxXYZ = BoundingBoxXYZ()
        minPoint = boundingBox.MinPoint
        maxPoint = boundingBox.MaxPoint
        boundingBoxXYZ.Min = XYZ(minPoint.X - 2, minPoint.Y - 2, minPoint.Z - 2)
        boundingBoxXYZ.Max = XYZ(maxPoint.X + 2, maxPoint.Y + 2, maxPoint.Z + 2)
        view.SetSectionBox(boundingBoxXYZ)
        outList.append(view)
    except Exception, e:
        outList.append(e)

TransactionManager.Instance.TransactionTaskDone()

OUT = outList

