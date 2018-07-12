import clr

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
elements = UnwrapElement(elements)
phase = IN[1]
if isinstance(phase, list):
    phase = phase[0]
outList = []

TransactionManager.Instance.EnsureInTransaction(doc)

for element in elements:
    if element.CreatedPhaseId.Equals(ElementId(phase.Id)):
        outList.append("Equal")
    else:
        try:
            element.DemolishedPhaseId = ElementId(phase.Id)
            outList.append("Set")
        except Exception, e:
            outList.append(e)

TransactionManager.Instance.TransactionTaskDone()

OUT = outList
