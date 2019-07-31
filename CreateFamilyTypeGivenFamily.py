import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
family = UnwrapElement(IN[0])
familyTypes = UnwrapElement(IN[1])
parameters = UnwrapElement(IN[2])
values = UnwrapElements(IN[3])

TransactionManager.Instance.EnsureInTransaction(doc)
for family in families:
    for familyType, parameter, value in zip(familyTypes, parameters, values):
        family.Symbol =
TransactionManager.Instance.TransactionTaskDone()
