import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

if not isinstance(IN[0], list):
    viewsIn = [IN[0]]
else:
    viewsIn = IN[0]

views = []
for i in viewsIn:
        views.append(UnwrapElement(i))

outList = []
for view in views:
    try:
        outList.append(view.IsTemplate)
    except:
        outList.append(False)

OUT = outList
