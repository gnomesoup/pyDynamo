import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

familySymbols = UnwrapElement(IN[0])
if not isinstance(familySymbols, list):
    familySymbols = [familySymbols]

newNames = IN[1]
if not isinstance(newNames, list):
    newNames = [newNames]

outList = []

TransactionManager.Instance.EnsureInTransaction(doc)

for familySymbol, newName  in zip(familySymbols, newNames):
    try:
        familySymbol.Name = newName
        outList.append(familySymbol)
    except:
        outList.append("Family does not exist")

TransactionManager.Instance.TransactionTaskDone()

OUT = outList
