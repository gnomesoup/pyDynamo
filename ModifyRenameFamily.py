import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

families = UnwrapElement(IN[0])
if not isinstance(families, list):
    families = [families]

newNames = IN[1]
if not isinstance(newNames, list):
    newNames = [newNames]

outList = []

TransactionManager.Instance.EnsureInTransaction(doc)

for family, newName  in zip(families, newNames):
    try:
        family.Name = newName
        outList.append(family)
    except Exception, e:
        outList.append("Family does not exist")

TransactionManager.Instance.TransactionTaskDone()

OUT = outList
