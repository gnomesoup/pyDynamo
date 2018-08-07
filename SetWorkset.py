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

# we pass in the workset id instead of the actual workset object
# because python will not convert them to objects using ToDSType
worksetId = IN[1]
if isinstance(worksetId, list):
    worksetId = worksetId[0]

outList = []

if doc.IsWorkshared:
    TransactionManager.Instance.EnsureInTransaction(doc)
    for element in elements:
        try:
            worksetParameter = element.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
            worksetParameter.Set(int(str(worksetId)))
            try:
                outList.append(element.ToDSType(True))
            except:
                outList.append(element)
        except Exception, e:
            outList.append(e)
    TransactionManager.Instance.TransactionTaskDone()
else:
    outList.append("Project is not workshared")

OUT = outList
