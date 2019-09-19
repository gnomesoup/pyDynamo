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
    elements = [IN[0]]
else:
    elements = IN[0]

elements = UnwrapElement(elements)

ownerView = False
viewId = False

outList = []
for element in elements:
    try:
        ownerView = element.View
    except Exception as e:
        error = e
    if not ownerView:
        try:
            viewId = element.OwnerViewId
        except Exception as e:
            error = e
        if not viewId:
            outList.append(error)
        else:
            outList.append(viewId)
    else:
        outList.append(ownerView)

OUT = outList
