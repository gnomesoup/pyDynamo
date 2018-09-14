import clr
import sys

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

elements = IN[0]
if not isinstance(elements, list):
    elements = [elements]
parameterValues = IN[1]
if not isinstance(parameterValues, list):
    parameterValues = [parameterValues]
parameterName = IN[2]

outList = []

TransactionManager.Instance.EnsureInTransaction(doc)
for element, value in zip(UnwrapElement(elements), parameterValues):
    p = element.LookupParameter(parameterName)
    try:
        p.Set(value)
        try:
            outList.append(element.ToDSType(True))
        except:
            outList.append(element)
    except Exception, e:
        outList.append(e)
TransactionManager.Instance.TransactionTaskDone()

OUT = outList
