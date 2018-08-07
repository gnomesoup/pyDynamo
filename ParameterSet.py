import clr
import sys

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

doc = DocumentManager.Instance.CurrentDBDocument
app = DocumentManager.Instance.CurrentUIApplication.Application

uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

elements = IN[0]
parameterValues = IN[1]
parameterName = IN[2]

outList = []

for element, value in zip(UnwrapElement(elements), parameterValues):
    p = element.LookupParameter(parameterName)
    TransactionManager.Instance.EnsureInTransaction(doc)
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
